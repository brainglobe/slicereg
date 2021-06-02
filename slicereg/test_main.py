import pytest
from slicereg.main import launch_gui

@pytest.mark.gui
def test_main_assembles_without_errors(qtbot):
    window = launch_gui(create_qapp=False)
    qtbot.addWidget(window.qt_widget)
