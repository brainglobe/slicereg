from unittest.mock import Mock

from slicereg.utils import Signal


def test_signal_calls_slot_when_emitted():
    signal = Signal()
    fun = Mock()
    signal.connect(callback=fun)
    fun.assert_not_called()
    signal.emit()
    fun.assert_called_once()


def test_signal_emits_keyword_argments_to_slot():
    signal = Signal()
    fun = Mock()
    signal.connect(callback=fun)
    signal.emit(hello="world")
    fun.assert_called_with(hello="world")

    signal.emit(data=3)
    fun.assert_called_with(data=3)

    signal.emit(data1=10, data2="Hi")
    fun.assert_called_with(data1=10, data2="Hi")


def test_disconnecting_signal_stops_emitting_to_slot():
    signal = Signal()
    fun = Mock()
    signal.connect(callback=fun)
    signal.emit()
    fun.assert_called_once()

    signal.disconnect(callback=fun)
    signal.emit()
    fun.assert_called_once()


def test_signal_emits_to_multiple_slots():
    signal = Signal()
    fun1, fun2 = Mock(), Mock()
    signal.connect(fun1)
    signal.connect(fun2)
    signal.emit()
    assert fun1.call_count == 1
    assert fun2.call_count == 1

    fun3 = Mock()
    signal.connect(fun3)
    signal.emit()
    assert fun1.call_count == 2
    assert fun2.call_count == 2
    assert fun3.call_count == 1

    signal.disconnect(fun2)
    signal.emit()
    assert fun1.call_count == 3
    assert fun2.call_count == 2
    assert fun3.call_count == 2