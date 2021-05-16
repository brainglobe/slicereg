from unittest.mock import Mock

from slicereg.gui.app_model import AppModel
from slicereg.gui.main_window import MainWindowView, MainWindowViewModel


def test_gui_launches_without_errors(qtbot):
    view = MainWindowView(_model=MainWindowViewModel(_model=Mock(AppModel)))
    qtbot.addWidget(view.qt_widget)
