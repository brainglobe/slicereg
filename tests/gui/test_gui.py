from unittest.mock import Mock

from slicereg.gui.model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.gui.views.sidebar import SidebarView, SidebarViewModel
from slicereg.gui.views.slice import SliceView, SliceViewModel
from slicereg.gui.views.volume import VolumeView, VolumeViewModel
from slicereg.gui.views.window import MainWindow, MainWindowViewModel
from slicereg.gui.main import launch_gui


def test_gui_launches_without_errors(qtbot):
    app = MainWindow(model=MainWindowViewModel(_model=AppModel()))
    qtbot.addWidget(app.qt_widget)


def test_volume_view_launches_without_errors(qtbot):
    view = VolumeView(model=VolumeViewModel(_model=AppModel(), _commands=Mock(CommandProvider)))
    qtbot.addWidget(view.qt_widget)


def test_slice_view_launches_without_errors(qtbot):
    view = SliceView(model=SliceViewModel(_model=AppModel(), _commands=Mock(CommandProvider)))
    qtbot.addWidget(view.qt_widget)


def test_sidebar_view_launches_without_errors(qtbot):
    view = SidebarView(model=SidebarViewModel(_model=AppModel(), _commands=Mock(CommandProvider)))
    qtbot.addWidget(view.qt_widget)


def test_main_assembles_without_errors(qtbot):
    window = launch_gui(create_qapp=False)
    qtbot.addWidget(window.qt_widget)
