from unittest.mock import Mock

from slicereg.app.app_model import AppModel
from slicereg.gui.sidebar import SidebarView, SidebarViewModel


def test_sidebar_view_launches_without_errors(qtbot):
    view = SidebarView(SidebarViewModel(_model=Mock(AppModel)))
    qtbot.addWidget(view.qt_widget)

