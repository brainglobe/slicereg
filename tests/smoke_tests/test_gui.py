import pytest

from slicereg.app.app_model import AppModel
from slicereg.gui.main_window import MainWindowViewModel
from slicereg.gui.main_window.view import MainWindowView
from slicereg.gui.sidebar import SidebarViewModel
from slicereg.gui.sidebar.view import SidebarView
from slicereg.gui.slice_window import SliceViewModel
from slicereg.gui.slice_window.view import SliceView
from slicereg.gui.volume_window import VolumeViewModel
from slicereg.gui.volume_window.view import VolumeView
from slicereg.main import launch_gui
from slicereg.utils import DependencyInjector


@pytest.fixture
def app_model():
    return AppModel(_injector=DependencyInjector())


def test_gui_launches_without_errors(qtbot, app_model):
    qtbot.addWidget(MainWindowView(_model=MainWindowViewModel(_model=app_model)).qt_widget)


def test_volume_view_launches_without_errors(qtbot, app_model):
    qtbot.addWidget(VolumeView(VolumeViewModel(_model=app_model)).qt_widget)


def test_slice_view_launches_without_errors(qtbot, app_model):
    qtbot.addWidget(SliceView(SliceViewModel(_model=app_model)).qt_widget)


def test_sidebar_view_launches_without_errors(qtbot, app_model):
    qtbot.addWidget(SidebarView(SidebarViewModel(app_model)).qt_widget)


def test_main_assembles_without_errors(qtbot):
    window = launch_gui(create_qapp=False)
    qtbot.addWidget(window.qt_widget)
