from dataclasses import dataclass, field
from typing import Optional, Dict
import time

@dataclass
class ContinuityContext:
    tenant_id: str
    user_id: str
    session_id: str
    sequence_id: int
    raw_input: str
    canon_anchor: Optional[str] = None
    waythread_state: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: float = field(default_factory=lambda: time.time())

class ContinuityControlPanel:
    """Foundational CCP implementation (Sections 1–3, 12)."""
    def __init__(self) -> None:
        self._last_sequence: Dict[tuple, int] = {}

    def _key(self, ctx: ContinuityContext) -> tuple:
        return (ctx.tenant_id, ctx.user_id, ctx.session_id)

    def validate_and_prepare(self, ctx: ContinuityContext) -> ContinuityContext:
        key = self._key(ctx)
        last_seq = self._last_sequence.get(key, 0)
        if ctx.sequence_id <= last_seq:
            ctx.sequence_id = last_seq + 1
        self._last_sequence[key] = ctx.sequence_id

        if ctx.canon_anchor is None:
            ctx.canon_anchor = "core.continuity"

        ctx.metadata.setdefault("ccp_validated", "true")
        return ctx
