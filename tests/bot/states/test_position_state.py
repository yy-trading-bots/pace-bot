import types
from typing import Any
import pytest
import bot.states.position_state as pos_module
from bot.states.position_state import PositionState


class Snapshot:
    def __init__(self, v: float) -> None:
        self.v = v

    def __str__(self) -> str:
        return f"Snapshot({self.v})"


class IndicatorManager:
    def __init__(self, to_return: Any) -> None:
        self._to_return = to_return

    def fetch_indicators(self) -> Any:
        return self._to_return


class BinanceAdapter:
    def __init__(self, im: IndicatorManager) -> None:
        self.indicator_manager = im


class DataManager:
    def __init__(self, snap: Any) -> None:
        self.market_snapshot = snap


class Parent:
    def __init__(self, snap: Any) -> None:
        self.data_manager = DataManager(snap)
        self.binance_adapter = BinanceAdapter(IndicatorManager(snap))


class ConcreteState(PositionState):
    def __init__(self, parent: Any) -> None:
        super().__init__(parent)
        self.called = False

    def apply(self) -> None:
        self.called = True


class RaisingState(PositionState):
    def apply(self) -> None:
        raise ValueError("boom")


def test_refresh_indicators_sets_snapshot():
    initial = Snapshot(1.0)
    updated = Snapshot(2.0)
    parent = Parent(initial)
    parent.binance_adapter.indicator_manager = IndicatorManager(updated)
    st = ConcreteState(parent=parent)
    st._refresh_indicators()
    assert parent.data_manager.market_snapshot is updated


def test_step_calls_refresh_and_apply_without_debug(monkeypatch):
    initial = Snapshot(10.0)
    updated = Snapshot(11.0)
    parent = Parent(initial)
    parent.binance_adapter.indicator_manager = IndicatorManager(updated)
    st = ConcreteState(parent=parent)
    logs = []
    monkeypatch.setattr(pos_module.Logger, "log_info", lambda m: logs.append(m))
    monkeypatch.setattr(pos_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    st.step()
    assert st.called is True
    assert parent.data_manager.market_snapshot is updated
    assert logs == []


def test_step_logs_debug_when_debug_true(monkeypatch):
    initial = Snapshot(5.0)
    updated = Snapshot(6.0)
    parent = Parent(initial)
    parent.binance_adapter.indicator_manager = IndicatorManager(updated)
    st = ConcreteState(parent=parent)
    logs = []
    monkeypatch.setattr(pos_module.Logger, "log_info", lambda m: logs.append(m))
    monkeypatch.setattr(pos_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=True))
    st.step()
    assert logs == [f"debug: {updated}"]
    assert st.called is True


def test_step_catches_exception_and_logs_exception(monkeypatch):
    initial = Snapshot(7.0)
    updated = Snapshot(8.0)
    parent = Parent(initial)
    parent.binance_adapter.indicator_manager = IndicatorManager(updated)
    st = RaisingState(parent=parent)
    errs = []
    monkeypatch.setattr(pos_module.Logger, "log_exception", lambda m: errs.append(m))
    monkeypatch.setattr(pos_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    st.step()
    assert errs == ["boom"]
    assert parent.data_manager.market_snapshot is updated
