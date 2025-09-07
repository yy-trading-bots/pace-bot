from bot.states.flat.short_base import ShortBase
from bot.states.flat.flat_position_state import FlatPositionState
from typing import Any
from bot.bot_settings import SETTINGS
from utils.logger import Logger


class ShortPendingState(ShortBase):
    """
    State representing a pending SHORT position.

    Responsibilities:
        - Mark the SHORT entry as pending by setting `is_pending = True`.
        - Log the state transition when DEBUG_MODE is enabled.
        - Transition to ShortConfirmedState on TP execution.
        - Transition to LongPendingState on SL execution.
    """

    def __init__(self, parent: Any) -> None:
        """
        Initialize the pending SHORT state.

        Args:
            parent (Any): The owning controller/state machine that provides shared
                resources (e.g., data_manager, exchange adapters) and holds the current state.
        """
        super().__init__(parent)
        self.is_pending = True
        if SETTINGS.DEBUG_MODE:
            Logger.log_info("STATE: SHORT PENDING STATE")

    def _set_tp_state(self) -> FlatPositionState:
        """
        Define the next state after Take-Profit (TP) execution.

        Returns:
            FlatPositionState: A new ShortConfirmedState instance created with the same
                parent, indicating the SHORT position is now confirmed.
        """
        from bot.states.flat.short_confirmed_state import ShortConfirmedState

        return ShortConfirmedState(self.parent)

    def _set_sl_state(self) -> FlatPositionState:
        """
        Define the next state after Stop-Loss (SL) execution.

        Returns:
            FlatPositionState: A new LongPendingState instance created with the same
                parent, indicating a reversal transition from SHORT to pending LONG.
        """
        from bot.states.flat.long_pending_state import LongPendingState

        return LongPendingState(self.parent)
