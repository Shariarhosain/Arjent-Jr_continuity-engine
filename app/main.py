from fastapi import FastAPI
from pydantic import BaseModel

from core.continuity.ccp import ContinuityControlPanel, ContinuityContext
from core.identity.models import IdentityContext
from core.canon.engine import CanonEngine
from core.waythread.engine import WayThreadEngine
from core.vaultdrive.engine import VaultDriveEngine
from core.ledger.engine import LedgerEngine
from core.execution.router import ExecutionRouter

app = FastAPI(title="Arjent Jr Enterprise – AutoLore Continuity Engine")

ccp = ContinuityControlPanel()
canon = CanonEngine()
waythread = WayThreadEngine()
vault = VaultDriveEngine()
ledger = LedgerEngine()
router = ExecutionRouter(
    ccp=ccp,
    canon=canon,
    waythread=waythread,
    vault=vault,
    ledger=ledger,
)

class InferenceRequest(BaseModel):
    tenant_id: str
    user_id: str
    session_id: str
    sequence_id: int
    message: str

class InferenceResponse(BaseModel):
    tenant_id: str
    user_id: str
    session_id: str
    sequence_id: int
    reply: str
    continuity_signature: dict

@app.get("/health")
async def health():
    return {"status": "ok", "engine": "arjent-jr-enterprise-1-15-final"}

@app.post("/infer", response_model=InferenceResponse)
async def infer(request: InferenceRequest):
    identity = IdentityContext(
        tenant_id=request.tenant_id,
        user_id=request.user_id,
        session_id=request.session_id,
    )
    ctx = ContinuityContext(
        tenant_id=identity.tenant_id,
        user_id=identity.user_id,
        session_id=identity.session_id,
        sequence_id=request.sequence_id,
        raw_input=request.message,
    )
    ctx = ccp.validate_and_prepare(ctx)
    result = router.handle_inference(ctx)
    resp = InferenceResponse(
        tenant_id=identity.tenant_id,
        user_id=identity.user_id,
        session_id=identity.session_id,
        sequence_id=ctx.sequence_id,
        reply=result.reply,
        continuity_signature=result.continuity_signature,
    )
    return resp
