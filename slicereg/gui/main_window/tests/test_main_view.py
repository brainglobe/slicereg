from unittest.mock import Mock

from slicereg.gui.app_model import AppModel
from slicereg.gui.main_window import MainWindowView, MainWindowViewModel
from slicereg.utils.introspection import get_public_attrs


def test_gui_launches_without_errors(qtbot):
    view = MainWindowView(_model=MainWindowViewModel(_model=Mock(AppModel)))
    qtbot.addWidget(view.qt_widget)


def test_main_view_updates_without_error_for_all_viewmodel_fields(qtbot):
    for attr in get_public_attrs(MainWindowViewModel):
        model = MainWindowViewModel(_model=Mock(AppModel))
        view = MainWindowView(_model=model)
        qtbot.addWidget(view.qt_widget)
        setattr(model, attr, getattr(model, attr))  # set attribute with its own value
