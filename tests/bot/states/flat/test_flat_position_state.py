import pytest
from typing import Any, cast
from bot.states.flat.flat_position_state import FlatPositionState


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


class ConcreteFlat(FlatPositionState):
    def apply(self) -> None:
        return None

    def _set_tp_state(self) -> FlatPositionState:
        return cast(FlatPositionState, object())

    def _set_sl_state(self) -> FlatPositionState:
        return cast(FlatPositionState, object())


def test_update_position_snapshot_clones_and_is_independent():
    parent = Parent(price=100.0)
    inst = ConcreteFlat(parent=parent)
    inst._update_position_snapshot()
    ps = parent.data_manager.position_snapshot
    assert ps is not None
    assert ps is not parent.data_manager.market_snapshot
    assert ps.price == 100.0
    parent.data_manager.market_snapshot.price = 150.0
    assert ps.price == 100.0


def test_calling_base_abstract_methods_via_super_returns_none():
    parent = Parent(price=50.0)
    inst = ConcreteFlat(parent=parent)
    assert super(ConcreteFlat, inst)._set_tp_state() is None
    assert super(ConcreteFlat, inst)._set_sl_state() is None
