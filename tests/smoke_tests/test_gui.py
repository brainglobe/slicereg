from slicereg.main import launch_gui
from slicereg.gui.sidebar.view import SidebarView
from slicereg.gui.slice_window.view import SliceView
from slicereg.gui.volume_window.view import VolumeView
from slicereg.gui.main_window.view import MainWindowView


def test_gui_launches_without_errors(qtbot):
    qtbot.addWidget(MainWindowView().qt_widget)


def test_volume_view_launches_without_errors(qtbot):
    qtbot.addWidget(VolumeView().qt_widget)


def test_slice_view_launches_without_errors(qtbot):
    qtbot.addWidget(SliceView().qt_widget)


def test_sidebar_view_launches_without_errors(qtbot):
    qtbot.addWidget(SidebarView().qt_widget)


def test_main_assembles_without_errors(qtbot):
    window = launch_gui(create_qapp=False)
    qtbot.addWidget(window.qt_widget)
