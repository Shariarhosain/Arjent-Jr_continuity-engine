from dataclasses import dataclass
from typing import Dict, List
import hashlib
import time
from ..continuity.ccp import ContinuityContext

@dataclass
class LedgerEntry:
    tenant_id: str
    user_id: str
    session_id: str
    sequence_id: int
    hash: str
    parent_hash: str
    created_at: float
    metadata: Dict[str, str]

class LedgerEngine:
    """Simple in-memory ledger with hash chaining."""

    def __init__(self) -> None:
        self._entries: List[LedgerEntry] = []
        self._last_hash_per_session: Dict[tuple, str] = {}

    def _session_key(self, ctx: ContinuityContext) -> tuple:
        return (ctx.tenant_id, ctx.user_id, ctx.session_id)

    def _compute_hash(self, payload: str, parent_hash: str) -> str:
        h = hashlib.sha256()
        h.update(parent_hash.encode("utf-8"))
        h.update(payload.encode("utf-8"))
        return h.hexdigest()

    def record(self, ctx: ContinuityContext, reply: str) -> LedgerEntry:
        key = self._session_key(ctx)
        parent = self._last_hash_per_session.get(key, "GENESIS")
        payload = f"{ctx.tenant_id}|{ctx.user_id}|{ctx.session_id}|{ctx.sequence_id}|{ctx.raw_input}|{reply}"
        h = self._compute_hash(payload, parent)
        entry = LedgerEntry(
            tenant_id=ctx.tenant_id,
            user_id=ctx.user_id,
            session_id=ctx.session_id,
            sequence_id=ctx.sequence_id,
            hash=h,
            parent_hash=parent,
            created_at=time.time(),
            metadata=dict(ctx.metadata),
        )
        self._entries.append(entry)
        self._last_hash_per_session[key] = h
        return entry

    def reconstruct_sequence(self, tenant_id: str, user_id: str, session_id: str) -> List[LedgerEntry]:
        return [
            e for e in self._entries
            if e.tenant_id == tenant_id and e.user_id == user_id and e.session_id == session_id
        ]
