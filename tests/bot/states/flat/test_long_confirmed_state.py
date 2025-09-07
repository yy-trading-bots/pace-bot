import types
from bot.states.flat.long_confirmed_state import LongConfirmedState
import bot.states.flat.long_confirmed_state as lc_module
from bot.states.flat.flat_position_state import FlatPositionState


class Parent:
    def __init__(self) -> None:
        pass


def test_init_sets_not_pending_and_logs_when_debug(monkeypatch):
    logs = []
    monkeypatch.setattr(lc_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=True))
    monkeypatch.setattr(lc_module.Logger, "log_info", lambda m: logs.append(m))
    parent = Parent()
    inst = LongConfirmedState(parent=parent)
    assert inst.is_pending is False
    assert logs == ["STATE: LONG CONFIRMED STATE"]


def test_init_no_log_when_not_debug(monkeypatch):
    logs = []
    monkeypatch.setattr(lc_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    monkeypatch.setattr(lc_module.Logger, "log_info", lambda m: logs.append(m))
    parent = Parent()
    inst = LongConfirmedState(parent=parent)
    assert inst.is_pending is False
    assert logs == []


def test_set_tp_state_returns_new_long_confirmed(monkeypatch):
    monkeypatch.setattr(lc_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    parent = Parent()
    inst = LongConfirmedState(parent=parent)
    nxt = inst._set_tp_state()
    assert isinstance(nxt, FlatPositionState)
    assert nxt is not inst
    assert nxt.__class__.__name__ == "LongConfirmedState"
    assert nxt.parent is parent


def test_set_sl_state_returns_long_pending(monkeypatch):
    monkeypatch.setattr(lc_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    parent = Parent()
    inst = LongConfirmedState(parent=parent)
    nxt = inst._set_sl_state()
    assert isinstance(nxt, FlatPositionState)
    assert nxt.__class__.__name__ == "LongPendingState"
    assert nxt.parent is parent
