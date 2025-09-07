from bot.states.flat.long_base import LongBase
from bot.states.flat.flat_position_state import FlatPositionState
from typing import Any
from bot.bot_settings import SETTINGS
from utils.logger import Logger


class LongPendingState(LongBase):
    """
    State representing a pending LONG position.

    This state indicates that the LONG entry is not yet fully confirmed
    (awaiting confirmation or order fill). It inherits behavior from
    LongBase but sets `is_pending` to True.

    Responsibilities:
        - Marks the LONG position as pending.
        - Logs state transition when DEBUG_MODE is active.
        - Defines transitions when TP or SL triggers while still pending.
    """

    def __init__(self, parent: Any) -> None:
        """
        Initialize the LongPendingState.

        Args:
            parent (Any): The parent object (usually a trading state
                          machine or controller) that provides shared
                          resources like data_manager and exchange adapter.
        """
        super().__init__(parent)
        self.is_pending = True
        if SETTINGS.DEBUG_MODE:
            Logger.log_info("STATE: LONG PENDING STATE")

    def _set_tp_state(self) -> FlatPositionState:
        """
        Define the next state after Take-Profit (TP) execution.

        Returns:
            FlatPositionState: A new LongConfirmedState instance,
                               indicating that the LONG position
                               has transitioned from pending to
                               confirmed.
        """
        from bot.states.flat.long_confirmed_state import LongConfirmedState

        return LongConfirmedState(self.parent)

    def _set_sl_state(self) -> FlatPositionState:
        """
        Define the next state after Stop-Loss (SL) execution.

        Returns:
            FlatPositionState: A new ShortPendingState instance,
                               indicating a reversal transition from
                               pending LONG to pending SHORT.
        """
        from bot.states.flat.short_pending_state import ShortPendingState

        return ShortPendingState(self.parent)
