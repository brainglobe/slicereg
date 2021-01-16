from time import sleep

from slicereg.gui.slice_view import SliceView
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.window import MainWindow


def test_gui_launches_without_errors(qtbot):
    app = MainWindow()
    qtbot.addWidget(app.qt_widget)


def test_volume_view_launches_without_errors(qtbot):
    view = VolumeView()
    qtbot.addWidget(view.qt_widget)


def test_slice_view_launches_without_errors(qtbot):
    view = SliceView()
    qtbot.addWidget(view.qt_widget)