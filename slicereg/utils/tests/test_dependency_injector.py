import pytest

from slicereg.utils import DependencyInjector


@pytest.mark.parametrize("val", [1, [], (), {'h': 3}, 3.2, None])
def test_di_container_attaches_same_object_to_function(val):
    container = DependencyInjector(obj=val)

    def fun(obj):
        return obj

    result = container.build(fun)
    assert result is val


def test_di_container_assigns_same_keyword_arg_to_obj():
    a, b, c = 3, 5, 2
    container = DependencyInjector(a=3, b=5, c=2)

    def fun(c, a=None, b=10):
        return a, b, c

    result = container.build(fun)
    assert result == (a, b, c)



def test_di_container_builds_classes():
    a, b, c = 3, 5, 2
    container = DependencyInjector(a=3, b=5, c=2)

    class Class:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

    klass = container.build(Class)
    assert klass.a is a
    assert klass.b is b
    assert klass.c is c


def test_di_container_assigns_subset_of_params():
    a, b, c = 3, 5, 2
    container = DependencyInjector(a=3, b=5, c=2)

    def fun(b, c):
        return b, c

    result = container.build(fun)
    assert result == (b, c)

    def fun2(a, c):
        return a, c

    result = container.build(fun2)
    assert result == (a, c)

