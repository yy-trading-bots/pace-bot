from bot.states.flat.flat_position_state import FlatPositionState
from utils.logger import Logger
from typing import final
from bot.bot_settings import SETTINGS


class ShortBase(FlatPositionState):
    """
    Base state that defines the common workflow for opening a SHORT position.

    Responsibilities:
        - Update and save the position snapshot.
        - Place TP/SL orders through the exchange adapter.
        - Log entry details and state information.
        - Transition to ShortPositionState with TP/SL targets.
    """

    def _apply_short(self) -> None:
        """
        Open a SHORT position and transition to the ShortPositionState.

        Actions performed:
            - Blocks further SHORT entries until the position is closed.
            - Saves a position snapshot.
            - Places TP/SL via the exchange adapter (in non-test mode).
            - Logs entry details.
        """
        self._update_position_snapshot()

        price: float = self.parent.data_manager.position_snapshot.price
        tp_price, sl_price = self.parent.binance_adapter.enter_short(
            price, state_block=self.is_pending
        )

        if not self.is_pending or SETTINGS.DEBUG_MODE:
            Logger.log_info(
                "Entered SHORT"
                + (
                    " | Confirmed: " + str(not self.is_pending)
                    if SETTINGS.DEBUG_MODE
                    else ""
                )
                + " | Current: "
                + str(round(price, 2))
                + " | TP_PRICE: "
                + str(round(tp_price, 2))
                + " | SL_PRICE: "
                + str(round(sl_price, 2))
            )
            Logger.log_info(str(self.parent.data_manager.position_snapshot))

        from bot.states.active.short_position_state import ShortPositionState

        self.parent.state = ShortPositionState(
            parent=self.parent, previous_state=self, target_prices=[tp_price, sl_price]
        )

    @final
    def apply(self) -> None:
        """
        Apply the trading logic for this position state.

        This method is final and cannot be overridden by subclasses.
        It delegates execution to `_apply_short()`, which handles
        the actual short entry workflow and state transition.
        """
        self._apply_short()
