import inspect
from typing import Callable, List
from unittest.mock import Mock

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

