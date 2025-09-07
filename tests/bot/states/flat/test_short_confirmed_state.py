import types
from bot.states.flat.short_confirmed_state import ShortConfirmedState
import bot.states.flat.short_confirmed_state as sc_module
from bot.states.flat.flat_position_state import FlatPositionState


class Parent:
    def __init__(self) -> None:
        pass


def test_init_sets_not_pending_and_logs_when_debug(monkeypatch):
    logs = []
    monkeypatch.setattr(sc_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=True))
    monkeypatch.setattr(sc_module.Logger, "log_info", lambda m: logs.append(m))
    parent = Parent()
    inst = ShortConfirmedState(parent=parent)
    assert inst.is_pending is False
    assert logs == ["STATE: SHORT CONFIRMED STATE"]


def test_init_no_log_when_not_debug(monkeypatch):
    logs = []
    monkeypatch.setattr(sc_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    monkeypatch.setattr(sc_module.Logger, "log_info", lambda m: logs.append(m))
    parent = Parent()
    inst = ShortConfirmedState(parent=parent)
    assert inst.is_pending is False
    assert logs == []


def test_set_tp_state_returns_new_short_confirmed(monkeypatch):
    monkeypatch.setattr(sc_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    parent = Parent()
    inst = ShortConfirmedState(parent=parent)
    nxt = inst._set_tp_state()
    assert isinstance(nxt, FlatPositionState)
    assert nxt is not inst
    assert nxt.__class__.__name__ == "ShortConfirmedState"
    assert nxt.parent is parent


def test_set_sl_state_returns_short_pending(monkeypatch):
    monkeypatch.setattr(sc_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    parent = Parent()
    inst = ShortConfirmedState(parent=parent)
    nxt = inst._set_sl_state()
    assert isinstance(nxt, FlatPositionState)
    assert nxt.__class__.__name__ == "ShortPendingState"
    assert nxt.parent is parent
