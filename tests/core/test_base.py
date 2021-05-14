from dataclasses import dataclass

from slicereg.core.base import FrozenUpdater


def test_updater_mixin_updates_dataframes():
    @dataclass(frozen=True)
    class A(FrozenUpdater):
        a: int
        b: int
        c: float

    a = A(3, 4, 5)
    a2 = a.update(a=33)
    assert a2.a == 33


def test_updater_mixin_updates_dataframes():
    @dataclass(frozen=True)
    class A(FrozenUpdater):
        a: int
        b: int
        c: float

    a = A(3, 4, 5)
    a2 = a.update(a=33, c=2)
    assert a2.a == 33 and a2.c == 2


def test_updater_works_on_nested_dataframes_one_level_down():

    @dataclass(frozen=True)
    class A(FrozenUpdater):
        a: int


    @dataclass(frozen=True)
    class B(FrozenUpdater):
        a: int
        b: A

    b = B(a=3, b=A(10))
    assert b.b.a == 10

    b2 = b.update(b__a=100)
    assert b2.b.a == 100