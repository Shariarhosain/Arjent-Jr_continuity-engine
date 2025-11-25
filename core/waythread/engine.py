from dataclasses import dataclass
from ..continuity.ccp import ContinuityContext

@dataclass
class WayThreadState:
    direction: str
    significance: float
    arc_state: str

class WayThreadEngine:
    """WayThread Lite + simplified Full (Sections 4–5, 10, 11)."""

    def __init__(self) -> None:
        self._default_direction = "steady"
        self._default_significance = 0.4
        self._default_arc = "plateau"

    def update_motion(self, ctx: ContinuityContext) -> WayThreadState:
        if ctx.sequence_id == 1:
            direction = "ascent"
            arc = "ascent"
            sig = 0.6
        elif ctx.sequence_id % 5 == 0:
            direction = "reflection"
            arc = "reflection"
            sig = 0.7
        else:
            direction = self._default_direction
            arc = self._default_arc
            sig = self._default_significance

        state = WayThreadState(direction=direction, significance=sig, arc_state=arc)
        ctx.waythread_state.update(
            {
                "direction": direction,
                "significance": sig,
                "arc_state": arc,
            }
        )
        return state
