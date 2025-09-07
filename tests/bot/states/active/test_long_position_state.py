from typing import Any, cast
from bot.states.active.long_position_state import LongPositionState
from bot.states.flat.flat_position_state import FlatPositionState


class Snapshot:
    def __init__(self, price: float) -> None:
        self.price = price


class DataManager:
    def __init__(self, snapshot: Snapshot) -> None:
        self.market_snapshot = snapshot


class Parent:
    def __init__(self, price: float) -> None:
        self.data_manager = DataManager(Snapshot(price))


class FakePrevState:
    def __init__(self, parent: Any) -> None:
        self.parent = parent
        self.is_pending = False

    def _set_tp_state(self):
        return object()

    def _set_sl_state(self):
        return object()


def make_lps(price: float, tp: float, sl: float) -> LongPositionState:
    parent = Parent(price=price)
    prev = FakePrevState(parent)
    return LongPositionState(
        parent=parent,
        previous_state=cast(FlatPositionState, prev),
        target_prices=[tp, sl],
    )


def test_is_tp_price_true_and_boundary():
    lps = make_lps(price=101.0, tp=100.0, sl=90.0)
    assert lps._is_tp_price() is True
    lps.parent.data_manager.market_snapshot.price = 100.0
    assert lps._is_tp_price() is False


def test_is_sl_price_true_and_boundary():
    lps = make_lps(price=89.0, tp=150.0, sl=90.0)
    assert lps._is_sl_price() is True
    lps.parent.data_manager.market_snapshot.price = 90.0
    assert lps._is_sl_price() is False


def test_apply_triggers_tp_branch(monkeypatch):
    lps = make_lps(price=160.0, tp=150.0, sl=80.0)
    calls = {}

    def fake_close(side, handler):
        calls["side"] = side
        calls["handler"] = handler

    monkeypatch.setattr(lps, "_close_position", fake_close)
    lps.apply()
    assert calls["side"] == "LONG"
    assert calls["handler"].__name__ == "_handle_tp"
    assert getattr(calls["handler"], "__self__", None) is lps


def test_apply_triggers_sl_branch_when_no_tp(monkeypatch):
    lps = make_lps(price=70.0, tp=150.0, sl=80.0)
    calls = {}

    def fake_close(side, handler):
        calls["side"] = side
        calls["handler"] = handler

    monkeypatch.setattr(lps, "_close_position", fake_close)
    lps.apply()
    assert calls["side"] == "LONG"
    assert calls["handler"].__name__ == "_handle_sl"
    assert getattr(calls["handler"], "__self__", None) is lps


def test_apply_no_action_when_neither_condition(monkeypatch):
    lps = make_lps(price=120.0, tp=150.0, sl=100.0)
    called = {"n": 0}

    def fake_close(*_args, **_kwargs):
        called["n"] += 1

    monkeypatch.setattr(lps, "_close_position", fake_close)
    lps.apply()
    assert called["n"] == 0


def test_apply_prefers_tp_when_both_true(monkeypatch):
    lps = make_lps(price=150.0, tp=100.0, sl=200.0)
    calls = {}

    def fake_close(side, handler):
        calls["side"] = side
        calls["handler"] = handler

    monkeypatch.setattr(lps, "_close_position", fake_close)
    lps.apply()
    assert calls["side"] == "LONG"
    assert calls["handler"].__name__ == "_handle_tp"
    assert getattr(calls["handler"], "__self__", None) is lps
