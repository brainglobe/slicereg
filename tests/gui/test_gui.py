from unittest.mock import Mock

from slicereg.gui.commands import CommandProvider
from slicereg.gui.sidebar_view import SidebarView
from slicereg.gui.slice_view import SliceView
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.window import MainWindow
from slicereg.main import launch_gui


def test_gui_launches_without_errors(qtbot):
    app = MainWindow()
    qtbot.addWidget(app.qt_widget)


def test_volume_view_launches_without_errors(qtbot):
    view = VolumeView(commands=Mock(CommandProvider))
    qtbot.addWidget(view.qt_widget)


def test_slice_view_launches_without_errors(qtbot):
    view = SliceView(commands=Mock(CommandProvider))
    qtbot.addWidget(view.qt_widget)


def test_sidebar_view_launches_without_errors(qtbot):
    view = SidebarView(commands=Mock(CommandProvider))
    qtbot.addWidget(view.qt_widget)


def test_main_assembles_without_errors(qtbot):
    window = launch_gui(create_qapp=False, load_atlas_on_launch=False)
    qtbot.addWidget(window.qt_widget)
