from slicereg.gui.main import launch_gui
from slicereg.gui.views.sidebar import SidebarView
from slicereg.gui.views.slice import SliceView
from slicereg.gui.views.volume import VolumeView
from slicereg.gui.views.main_window import MainWindow


def test_gui_launches_without_errors(qtbot):
    qtbot.addWidget(MainWindow().qt_widget)


def test_volume_view_launches_without_errors(qtbot):
    qtbot.addWidget(VolumeView().qt_widget)


def test_slice_view_launches_without_errors(qtbot):
    qtbot.addWidget(SliceView().qt_widget)


def test_sidebar_view_launches_without_errors(qtbot):
    qtbot.addWidget(SidebarView().qt_widget)


def test_main_assembles_without_errors(qtbot):
    window = launch_gui(create_qapp=False)
    qtbot.addWidget(window.qt_widget)
