import types
import pytest
from typing import cast, Any
import bot.pace_bot as pace_bot_module
from bot.pace_bot import PaceBot


class FakePerformanceTracker:
    def __init__(self) -> None:
        self.inited = True


class FakeDataManager:
    def __init__(self) -> None:
        self.inited = True


class FakeBinanceAdapter:
    def __init__(self) -> None:
        self.inited = True


class FakeState:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.step_calls = 0

    def step(self) -> None:
        self.step_calls += 1


def test_init_sets_dependencies_and_initial_state_and_logs(monkeypatch):
    logs = []
    monkeypatch.setattr(pace_bot_module, "PerformanceTracker", FakePerformanceTracker)
    monkeypatch.setattr(pace_bot_module, "DataManager", FakeDataManager)
    monkeypatch.setattr(pace_bot_module, "BinanceAdapter", FakeBinanceAdapter)
    monkeypatch.setattr(pace_bot_module, "LongPendingState", FakeState)
    monkeypatch.setattr(pace_bot_module.Logger, "log_start", lambda m: logs.append(m))
    bot = PaceBot()
    assert isinstance(bot.performance_tracker, FakePerformanceTracker)
    assert isinstance(bot.data_manager, FakeDataManager)
    assert isinstance(bot.binance_adapter, FakeBinanceAdapter)
    assert isinstance(bot.state, FakeState)
    assert bot.state.parent is bot
    assert logs == ["PaceBot is running..."]


def test_run_exits_when_sleep_raises_and_sleep_called_once(monkeypatch):
    calls = []

    class StopLoop(Exception):
        pass

    def fake_sleep(seconds: float) -> None:
        calls.append(seconds)
        raise StopLoop

    monkeypatch.setattr(pace_bot_module, "LongPendingState", FakeState)
    monkeypatch.setattr(pace_bot_module, "sleep", fake_sleep)
    monkeypatch.setattr(
        pace_bot_module, "SETTINGS", types.SimpleNamespace(SLEEP_DURATION=1.23)
    )
    # Prevent real network calls inside BinanceAdapter()
    monkeypatch.setattr(pace_bot_module, "BinanceAdapter", FakeBinanceAdapter)

    bot = PaceBot()
    with pytest.raises(StopLoop):
        bot.run()
    assert calls == [1.23]
    assert cast(Any, bot.state).step_calls == 0


def test_run_exits_when_step_raises_and_sleep_called_once(monkeypatch):
    sleep_calls = []

    def fake_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)

    class StopLoop(Exception):
        pass

    class RaisingState(FakeState):
        def step(self) -> None:
            super().step()
            raise StopLoop

    monkeypatch.setattr(pace_bot_module, "LongPendingState", RaisingState)
    monkeypatch.setattr(pace_bot_module, "sleep", fake_sleep)
    monkeypatch.setattr(
        pace_bot_module, "SETTINGS", types.SimpleNamespace(SLEEP_DURATION=2.5)
    )
    # Prevent real network calls inside BinanceAdapter()
    monkeypatch.setattr(pace_bot_module, "BinanceAdapter", FakeBinanceAdapter)

    bot = PaceBot()
    with pytest.raises(StopLoop):
        bot.run()
    assert sleep_calls == [2.5]
    assert cast(Any, bot.state).step_calls == 1
