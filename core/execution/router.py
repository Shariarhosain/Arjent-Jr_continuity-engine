from dataclasses import dataclass
from typing import Dict

from ..continuity.ccp import ContinuityContext
from ..canon.engine import CanonEngine
from ..waythread.engine import WayThreadEngine
from ..vaultdrive.engine import VaultDriveEngine
from ..ledger.engine import LedgerEngine

@dataclass
class ExecutionResult:
    reply: str
    continuity_signature: Dict[str, str]

class ExecutionRouter:
    """Top-level execution orchestration."""

    def __init__(
        self,
        ccp,
        canon: CanonEngine,
        waythread: WayThreadEngine,
        vault: VaultDriveEngine,
        ledger: LedgerEngine,
    ) -> None:
        self._canon = canon
        self._waythread = waythread
        self._vault = vault
        self._ledger = ledger

    def handle_inference(self, ctx: ContinuityContext) -> ExecutionResult:
        motion = self._waythread.update_motion(ctx)
        draft_reply = f"You said: '{ctx.raw_input}'. Continuity preserved."
        final_reply = self._canon.enforce(ctx, draft_reply)
        self._vault.write_record(ctx, content=final_reply, class_label="B")
        entry = self._ledger.record(ctx, reply=final_reply)
        signature = {
            "direction": ctx.waythread_state.get("direction", ""),
            "significance": str(ctx.waythread_state.get("significance", "")),
            "arc_state": ctx.waythread_state.get("arc_state", ""),
            "ledger_hash": entry.hash,
            "parent_hash": entry.parent_hash,
        }
        return ExecutionResult(reply=final_reply, continuity_signature=signature)
