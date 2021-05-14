from unittest.mock import Mock

from slicereg.utils.observable import HasObservableAttributes


def test_observable_calls_fun_when_attributes_are_modified():
    class A(HasObservableAttributes):
        def __init__(self):
            HasObservableAttributes.__init__(self)
            self.a = 3
            self.b = 5
            self.c = 10

    callback = Mock()
    observable = A()
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


