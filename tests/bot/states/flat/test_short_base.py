import types
import pytest
from typing import cast
from bot.states.flat.short_base import ShortBase
import bot.states.flat.short_base as sb_module
from bot.states.active.short_position_state import ShortPositionState


class Snapshot:
    def __init__(self, price: float) -> None:
        self.price = price

    def clone(self) -> "Snapshot":
        return Snapshot(self.price)


class DataManager:
    def __init__(self, snapshot: Snapshot) -> None:
        self.market_snapshot = snapshot
        self.position_snapshot: Snapshot | None = None


class Parent:
    def __init__(self, price: float) -> None:
        self.data_manager = DataManager(Snapshot(price))
        self.binance_adapter = types.SimpleNamespace()


class ConcreteShortBase(ShortBase):
    def _set_tp_state(self):
        return cast(ShortBase, self)

    def _set_sl_state(self):
        return cast(ShortBase, self)


def make_instance(
    price: float, tp_return: float, sl_return: float
) -> ConcreteShortBase:
    parent = Parent(price=price)

    def enter_short(p: float, state_block: bool):
        return tp_return, sl_return

    parent.binance_adapter.enter_short = enter_short
    return ConcreteShortBase(parent=parent)


def test_apply_not_pending_logs_and_sets_state(monkeypatch):
    inst = make_instance(price=321.0, tp_return=310.0, sl_return=335.0)
    inst.is_pending = False
    logs = []
    monkeypatch.setattr(sb_module.Logger, "log_info", lambda msg: logs.append(msg))
    monkeypatch.setattr(sb_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    inst.apply()
    assert isinstance(inst.parent.state, ShortPositionState)
    state = inst.parent.state
    assert state.tp_price == 310.0
    assert state.sl_price == 335.0
    assert state.previous_state is inst
    assert len(logs) == 2
    assert "Entered SHORT" in logs[0]
    assert "Confirmed:" not in logs[0]
    assert "TP_PRICE: 310.0" in logs[0]
    assert "SL_PRICE: 335.0" in logs[0]


def test_apply_pending_no_debug_no_logs(monkeypatch):
    inst = make_instance(price=200.0, tp_return=190.0, sl_return=210.0)
    inst.is_pending = True
    logs = []
    monkeypatch.setattr(sb_module.Logger, "log_info", lambda msg: logs.append(msg))
    monkeypatch.setattr(sb_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=False))
    inst.apply()
    assert isinstance(inst.parent.state, ShortPositionState)
    assert logs == []


def test_apply_pending_with_debug_logs_include_confirmed(monkeypatch):
    inst = make_instance(price=300.0, tp_return=295.0, sl_return=305.0)
    inst.is_pending = True
    logs = []
    monkeypatch.setattr(sb_module.Logger, "log_info", lambda msg: logs.append(msg))
    monkeypatch.setattr(sb_module, "SETTINGS", types.SimpleNamespace(DEBUG_MODE=True))
    inst.apply()
    assert isinstance(inst.parent.state, ShortPositionState)
    assert len(logs) == 2
    assert "Entered SHORT" in logs[0]
    assert "Confirmed: False" in logs[0]
    assert "TP_PRICE: 295.0" in logs[0]
    assert "SL_PRICE: 305.0" in logs[0]
