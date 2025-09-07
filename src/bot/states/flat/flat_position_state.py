from __future__ import annotations
from abc import abstractmethod
from bot.states.position_state import PositionState
from typing import final, Any


class FlatPositionState(PositionState):
    """
    State representing the absence of any active position.

    This state evaluates entry conditions for LONG or SHORT positions
    using the latest market snapshot and transitions to the
    appropriate active-position state when conditions are satisfied.
    """

    def __init__(self, parent: Any) -> None:
        """
        Initialize a PositionState.

        Args:
            parent (Any): The PaceBot object reference that manages trading logic,
                             containing shared resources like DataManager and BinanceAdapter.
        """
        super().__init__(parent)
        self.is_pending: bool

    @final
    def _update_position_snapshot(self) -> None:
        """
        Persist the current market snapshot as the position snapshot.

        This is used to record the market context at the moment the position
        is opened (price and technical indicators).
        """
        self.parent.data_manager.position_snapshot = (
            self.parent.data_manager.market_snapshot.clone()
        )

    @abstractmethod
    def _set_tp_state(self) -> FlatPositionState:
        pass

    @abstractmethod
    def _set_sl_state(self) -> FlatPositionState:
        pass
