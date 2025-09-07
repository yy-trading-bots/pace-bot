import types
from bot.states.flat.long_pending_state import LongPendingState
import bot.states.flat.long_pending_state as lp_module
from bot.states.flat.flat_position_state import FlatPositionState


class Parent:
    def __init__(self) -> None:
        pass


def test_init_sets_pending_and_logs_when_debug(monkeypatch):
    logs = []
    monkeypatch.setattr(lp_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=True))
    monkeypatch.setattr(lp_module.Logger, "log_info", lambda m: logs.append(m))
    parent = Parent()
    inst = LongPendingState(parent=parent)
    assert inst.is_pending is True
    assert logs == ["STATE: LONG PENDING STATE"]


def test_init_no_log_when_not_debug(monkeypatch):
    logs = []
    monkeypatch.setattr(lp_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    monkeypatch.setattr(lp_module.Logger, "log_info", lambda m: logs.append(m))
    parent = Parent()
    inst = LongPendingState(parent=parent)
    assert inst.is_pending is True
    assert logs == []


def test_set_tp_state_returns_long_confirmed(monkeypatch):
    monkeypatch.setattr(lp_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    parent = Parent()
    inst = LongPendingState(parent=parent)
    nxt = inst._set_tp_state()
    assert isinstance(nxt, FlatPositionState)
    assert nxt.__class__.__name__ == "LongConfirmedState"
    assert nxt is not inst
    assert nxt.parent is parent


def test_set_sl_state_returns_short_pending(monkeypatch):
    monkeypatch.setattr(lp_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    parent = Parent()
    inst = LongPendingState(parent=parent)
    nxt = inst._set_sl_state()
    assert isinstance(nxt, FlatPositionState)
    assert nxt.__class__.__name__ == "ShortPendingState"
    assert nxt.parent is parent
