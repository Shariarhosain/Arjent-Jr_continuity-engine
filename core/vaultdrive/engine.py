from dataclasses import dataclass
from typing import Dict, List
from ..continuity.ccp import ContinuityContext

@dataclass
class VaultRecord:
    tenant_id: str
    user_id: str
    session_id: str
    sequence_id: int
    content: str
    class_label: str

class VaultDriveEngine:
    """Minimal VaultDrive implementation (Section 6)."""

    def __init__(self) -> None:
        self._records: List[VaultRecord] = []

    def write_record(self, ctx: ContinuityContext, content: str, class_label: str = "B") -> None:
        rec = VaultRecord(
            tenant_id=ctx.tenant_id,
            user_id=ctx.user_id,
            session_id=ctx.session_id,
            sequence_id=ctx.sequence_id,
            content=content,
            class_label=class_label,
        )
        self._records.append(rec)

    def read_records_for_session(self, tenant_id: str, user_id: str, session_id: str) -> List[VaultRecord]:
        return [
            r
            for r in self._records
            if r.tenant_id == tenant_id and r.user_id == user_id and r.session_id == session_id
        ]
