from bot.states.flat.short_base import ShortBase
from bot.states.flat.flat_position_state import FlatPositionState
from typing import Any
from bot.bot_settings import SETTINGS
from utils.logger import Logger


class ShortConfirmedState(ShortBase):
    """
    State representing a confirmed SHORT position.

    Responsibilities:
        - Mark the position as confirmed by setting `is_pending = False`.
        - Log the state transition when DEBUG_MODE is enabled.
        - On TP, return a new ShortConfirmedState instance (reset same state type).
        - On SL, transition to ShortPendingState.
    """

    def __init__(self, parent: Any) -> None:
        """
        Initialize the confirmed SHORT state.

        Args:
            parent (Any): The owning controller/state machine that provides shared
                resources (e.g., data_manager, exchange adapters) and holds the current state.
        """
        super().__init__(parent)
        self.is_pending = False
        if SETTINGS.DEBUG_MODE:
            Logger.log_info("STATE: SHORT CONFIRMED STATE")

    def _set_tp_state(self) -> FlatPositionState:
        """
        Define the next state after Take-Profit (TP) execution.

        Returns:
            FlatPositionState: A new ShortConfirmedState instance created with the same
                parent, effectively resetting the confirmed SHORT state.
        """
        return ShortConfirmedState(parent=self.parent)

    def _set_sl_state(self) -> FlatPositionState:
        """
        Define the next state after Stop-Loss (SL) execution.

        Returns:
            FlatPositionState: A new ShortPendingState instance created with the same
                parent, indicating a transition to a pending SHORT state.
        """
        from bot.states.flat.short_pending_state import ShortPendingState

        return ShortPendingState(self.parent)
