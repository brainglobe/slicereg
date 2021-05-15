from unittest.mock import Mock, patch

import pytest

from slicereg.app.app_model import AppModel
from slicereg.gui.sidebar import SidebarView, SidebarViewModel


@pytest.fixture
def view_model():
    return SidebarViewModel(_model=Mock(AppModel))


@pytest.fixture
def view(view_model):
    return SidebarView(_model=view_model)


def test_sidebar_view_launches_without_errors(qtbot, view):
    qtbot.addWidget(view.qt_widget)


def test_sidebar_show_image_dialog_doesnt_crash(qtbot, view):
    qtbot.addWidget(view.qt_widget)
    with patch('slicereg.gui.sidebar.view.QFileDialog.getOpenFileName') as get_filename:
        get_filename.return_value = "myfile.tiff", ".tiff"
        view.show_load_image_dialog()


def test_sidebar_show_atlas_dialog_doesnt_crash(qtbot, view: SidebarView, view_model):
    qtbot.addWidget(view.qt_widget)
    view_model.atlas_resolution_text = "10"
    with patch('slicereg.gui.sidebar.view.QFileDialog.getOpenFileName') as get_filename:
        get_filename.return_value = "myfile.tiff", ".tiff"
        view.show_load_atlas_dialog()
