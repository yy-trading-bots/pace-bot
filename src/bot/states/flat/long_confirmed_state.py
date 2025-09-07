from bot.states.flat.long_base import LongBase
from bot.states.flat.flat_position_state import FlatPositionState
from typing import Any
from bot.bot_settings import SETTINGS
from utils.logger import Logger


class LongConfirmedState(LongBase):
    """
    State representing a confirmed LONG position.

    This state indicates that the LONG entry has been fully confirmed
    (not pending anymore). It inherits the LONG entry logic from
    LongBase but sets `is_pending` to False.

    Responsibilities:
        - Marks the position as confirmed.
        - Logs state transition in DEBUG_MODE.
        - Defines state transition behavior when TP or SL triggers.
    """

    def __init__(self, parent: Any) -> None:
        """
        Initialize the LongConfirmedState.

        Args:
            parent (Any): The parent object (usually a trading state
                          machine or controller) that holds shared
                          resources such as data_manager and adapters.
        """
        super().__init__(parent)
        self.is_pending = False
        if SETTINGS.DEBUG_MODE:
            Logger.log_info("STATE: LONG CONFIRMED STATE")

    def _set_tp_state(self) -> FlatPositionState:
        """
        Define the next state after Take-Profit (TP) execution.

        Returns:
            FlatPositionState: A new LongConfirmedState instance created
                            with the same parent. This effectively
                            resets the state while keeping the position
                            confirmed.
        """
        return LongConfirmedState(parent=self.parent)

    def _set_sl_state(self) -> FlatPositionState:
        """
        Define the next state after Stop-Loss (SL) execution.

        Returns:
            FlatPositionState: A new LongPendingState instance is
                               returned, indicating that the LONG
                               position transitions into a pending
                               state after SL.
        """
        from bot.states.flat.long_pending_state import LongPendingState

        return LongPendingState(self.parent)
