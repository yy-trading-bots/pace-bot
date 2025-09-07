from __future__ import annotations

from bot.performance_tracker import PerformanceTracker
from bot.data_manager import DataManager
from bot.states.flat.long_pending_state import LongPendingState
from bot.states.position_state import PositionState
from bot.bot_settings import SETTINGS
from binance_adapter.binance_adapter import BinanceAdapter
from utils.logger import Logger
from time import sleep


class PaceBot:
    """
    Core trading bot that manages state transitions, indicators,
    and interaction with the Binance API.

    The bot uses a state machine pattern where each trading
    position state (e.g., NoPosition, Long, Short) is represented
    by a dedicated class.
    """

    def __init__(self) -> None:
        """
        Initialize the PaceBot instance.

        Attributes:
            performance_tracker (PerformanceTracker): Tracks wins and losses.
            data_manager (DataManager): Manages market indicators and position snapshots.
            binance_adapter (BinanceAdapter): Interface for Binance API operations.
            state (PositionState): Current trading state of the bot.
        """
        self.performance_tracker: PerformanceTracker = PerformanceTracker()
        self.data_manager: DataManager = DataManager()
        self.binance_adapter: BinanceAdapter = BinanceAdapter()
        Logger.log_start("PaceBot is running...")
        self.state: PositionState = LongPendingState(parent=self)

    def run(self) -> None:
        """
        Start the trading loop.

        The loop executes indefinitely, with each iteration:
            - Sleeping for the configured duration.
            - Executing the current state's `step` method.
        """
        while True:
            sleep(SETTINGS.SLEEP_DURATION)
            self.state.step()
