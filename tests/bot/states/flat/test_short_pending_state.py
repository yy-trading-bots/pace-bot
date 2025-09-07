import types
from bot.states.flat.short_pending_state import ShortPendingState
import bot.states.flat.short_pending_state as sp_module
from bot.states.flat.flat_position_state import FlatPositionState


class Parent:
    def __init__(self) -> None:
        pass


def test_init_sets_pending_and_logs_when_debug(monkeypatch):
    logs = []
    monkeypatch.setattr(sp_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=True))
    monkeypatch.setattr(sp_module.Logger, "log_info", lambda m: logs.append(m))
    parent = Parent()
    inst = ShortPendingState(parent=parent)
    assert inst.is_pending is True
    assert logs == ["STATE: SHORT PENDING STATE"]


def test_init_no_log_when_not_debug(monkeypatch):
    logs = []
    monkeypatch.setattr(sp_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    monkeypatch.setattr(sp_module.Logger, "log_info", lambda m: logs.append(m))
    parent = Parent()
    inst = ShortPendingState(parent=parent)
    assert inst.is_pending is True
    assert logs == []


def test_set_tp_state_returns_short_confirmed(monkeypatch):
    monkeypatch.setattr(sp_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    parent = Parent()
    inst = ShortPendingState(parent=parent)
    nxt = inst._set_tp_state()
    assert isinstance(nxt, FlatPositionState)
    assert nxt.__class__.__name__ == "ShortConfirmedState"
    assert nxt is not inst
    assert nxt.parent is parent


def test_set_sl_state_returns_long_pending(monkeypatch):
    monkeypatch.setattr(sp_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    parent = Parent()
    inst = ShortPendingState(parent=parent)
    nxt = inst._set_sl_state()
    assert isinstance(nxt, FlatPositionState)
    assert nxt.__class__.__name__ == "LongPendingState"
    assert nxt.parent is parent
