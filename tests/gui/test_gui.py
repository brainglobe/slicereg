from unittest.mock import Mock

from slicereg.gui.model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.gui.sidebar_view import SidebarView, SidebarViewModel
from slicereg.gui.slice_view import SliceView, SliceViewModel
from slicereg.gui.volume_view import VolumeView, VolumeViewModel
from slicereg.gui.window import MainWindow
from slicereg.gui.main import launch_gui


def test_gui_launches_without_errors(qtbot):
    app = MainWindow()
    qtbot.addWidget(app.qt_widget)


def test_volume_view_launches_without_errors(qtbot):
    view = VolumeView(
        commands=Mock(CommandProvider),
        model=VolumeViewModel(_model=AppModel()),

    )
    qtbot.addWidget(view.qt_widget)


def test_slice_view_launches_without_errors(qtbot):
    view = SliceView(
        commands=Mock(CommandProvider),
        model=SliceViewModel(_model=AppModel()),
    )
    qtbot.addWidget(view.qt_widget)


def test_sidebar_view_launches_without_errors(qtbot):
    view = SidebarView(
        commands=Mock(CommandProvider),
        model=SidebarViewModel(_model=AppModel())
    )
    qtbot.addWidget(view.qt_widget)


def test_main_assembles_without_errors(qtbot):
    window = launch_gui(create_qapp=False)
    qtbot.addWidget(window.qt_widget)
