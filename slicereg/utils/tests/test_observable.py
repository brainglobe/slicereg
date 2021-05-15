from unittest.mock import Mock

import pytest

from slicereg.utils.observable import HasObservableAttributes


@pytest.fixture
def observable():
    class Observable(HasObservableAttributes):
        def __init__(self):
            HasObservableAttributes.__init__(self)
            self.a = 3
            self.b = 5
            self.c = 10

    return Observable()


def test_observable_calls_fun_when_attributes_are_modified(observable):
    callback = Mock()
    observable.register(callback)
    assert callback.call_count == 0

    observable.a = 10
    assert callback.call_count == 1
    assert callback.call_args[1] == {'changed': 'a'}

    observable.b = 2
    assert callback.call_count == 2
    assert callback.call_args[1] == {'changed': 'b'}

    observable.a = 2
    assert callback.call_count == 3
    assert callback.call_args[1] == {'changed': 'a'}

    observable.new_attr = 2
    assert callback.call_count == 4
    assert callback.call_args[1] == {'changed': 'new_attr'}


def test_observable_calls_all_registered_funs(observable):
    a, b, c = Mock(), Mock(), Mock()
    observable.register(a)
    observable.register(b)

    observable.x = 3
    assert a.call_args[1] == {'changed': 'x'}
    assert b.call_args[1] == {'changed': 'x'}
    assert c.call_count == 0


def test_observable_doesnt_emit_protected_nor_private_attrs(observable):
    a = Mock()
    observable.register(a)
    observable._x = 10
    assert a.call_count == 0

    observable.__x = 20
    assert a.call_count == 0
