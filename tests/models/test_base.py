from dataclasses import dataclass

from slicereg.models.base import FrozenUpdater


def test_setter_mixin_updates_dataframes():
    @dataclass(frozen=True)
    class A(FrozenUpdater):
        a: int
        b: int
        c: float

    a = A(3, 4, 5)
    a2 = a.update(a=33)
    assert a2.a == 33
