import inspect
from typing import Callable, List
from unittest.mock import Mock

from vispy.scene.events import SceneMouseEvent
from vispy.util.event import Event

from slicereg.app.app_model import AppModel
from slicereg.gui.slice_window import SliceView, SliceViewModel


def get_public_attrs(fun: Callable) -> List[str]:
    return [attr for attr in inspect.signature(fun).parameters if not attr.startswith('_')]


def test_slice_view_launches_without_errors(qtbot):
    model = SliceViewModel(_model=Mock(AppModel))
    view = SliceView(_model=model)
    qtbot.addWidget(view.qt_widget)


def test_slice_view_updates_without_error_for_all_viewmodel_fields(qtbot):
    for attr in get_public_attrs(SliceViewModel):
        model = SliceViewModel(_model=Mock(AppModel))
        view = SliceView(_model=model)
        qtbot.addWidget(view.qt_widget)
        setattr(model, attr, getattr(model, attr))  # set attribute with its own value


def test_slice_view_triggers_mouse_wheel_viewmodel_mouse_wheel(qtbot):
    model = Mock(SliceViewModel)
    view = SliceView(_model=model)
    qtbot.addWidget(view.qt_widget)

    event = Mock(SceneMouseEvent, delta=(1, 5))
    view.mouse_wheel(event)
    model.on_mousewheel_move.assert_called_with(increment=5)


def test_slice_view_triggers_left_mouse_drag_on_viewmodel(qtbot):
    model = Mock(SliceViewModel)
    view = SliceView(_model=model)
    qtbot.addWidget(view.qt_widget)

    event = Mock(SceneMouseEvent, pos=(5, 10), button=1)
    event.last_event.pos = (1, 2)
    view.mouse_move(event)
    model.on_left_mouse_drag.assert_called_with(x1=1, y1=2, x2=5, y2=10)
    model.on_right_mouse_drag.assert_not_called()


def test_slice_view_triggers_right_mouse_drag_on_viewmodel(qtbot):
    model = Mock(SliceViewModel)
    view = SliceView(_model=model)
    qtbot.addWidget(view.qt_widget)

    event = Mock(SceneMouseEvent, pos=(5, 10), button=2)
    event.last_event.pos = (1, 2)
    view.mouse_move(event)
    model.on_left_mouse_drag.assert_not_called()
    model.on_right_mouse_drag.assert_called_with(x1=1, y1=2, x2=5, y2=10)
