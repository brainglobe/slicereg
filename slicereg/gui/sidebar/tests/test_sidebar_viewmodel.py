from unittest.mock import Mock

import pytest
from hypothesis import given
from hypothesis.strategies import floats, text
from pytest import approx

from slicereg.app.app_model import AppModel
from slicereg.gui.sidebar.viewmodel import SidebarViewModel
from slicereg.utils import DependencyInjector


@pytest.fixture(scope='module')
def app_model():
    app_model = AppModel(_injector=Mock(DependencyInjector))
    return app_model


@pytest.fixture(scope='module')
def view_model(app_model):
    return SidebarViewModel(_model=app_model)


@given(resolution=floats(0.01, 100))
def test_resolution_updated_with_section_text_change(resolution, view_model: SidebarViewModel):
    view_model.section_resolution_text = str(resolution)
    assert view_model._model.section_image_resolution == approx(resolution)


def test_app_updates_with_None_when_viewmode_sets_resolution_to_empty_string(view_model: SidebarViewModel, app_model):
    view_model.section_resolution_text = ''
    assert view_model._model.section_image_resolution is None


@given(resolution=floats(0.01, 100))
def test_viewmodel_resolution_updated_when_app_updates(resolution, view_model: SidebarViewModel, app_model):
    app_model.section_image_resolution = resolution
    if resolution is None:
        assert view_model.section_resolution_text == ''
    else:
        assert view_model.section_resolution_text == str(resolution)


def test_viewmodel_resolution_is_emptry_string_when_app_is_none(view_model: SidebarViewModel, app_model):
    app_model.section_image_resolution = None
    assert view_model.section_resolution_text == ''


@given(text=text(alphabet="abcdefghijklmnopqrstuvwxyzäüö%&/()=?_'\"\\", min_size=1, max_size=10))
def test_viewmodel_resolution_text_does_not_accept_nonnumeric_strings(view_model, text):
    view_model.section_resolution_text = "3.1"
    view_model.section_resolution_text = text
    assert view_model.section_resolution_text == "3.1"


def test_viewmodel_bgatlas_dropdown_fills_with_atlas_names_when_app_gets_them(app_model, view_model: SidebarViewModel):
    atlases = ["atlas1", "mouse_atlas", "rat_atlas2"]
    app_model.bgatlas_names = atlases
    assert view_model.bgatlas_dropdown_entries == atlases


def test_clicking_coronal_orientation_button_tells_app_to_rotate_slice_to_coronal_orientation():
    app_model = Mock(AppModel)
    view_model = SidebarViewModel(_model=app_model)
    view_model.click_coronal_button()
    assert app_model.orient_section_to_coronal.call_count == 1


def test_clicking_axial_orientation_button_tells_app_to_rotate_slice_to_axial_orientation():
    app_model = Mock(AppModel)
    view_model = SidebarViewModel(_model=app_model)
    view_model.click_axial_button()
    assert app_model.orient_section_to_axial.call_count == 1


def test_clicking_sagittal_orientation_button_tells_app_to_rotate_slice_to_sagittal_orientation():
    app_model = Mock(AppModel)
    view_model = SidebarViewModel(_model=app_model)
    view_model.click_sagittal_button()
    assert app_model.orient_section_to_sagittal.call_count == 1


def test_moving_clim_section_2d_slider_sets_the_apps_clim_2d(app_model, view_model):
    clim = (0.3, 0.8)
    view_model.move_clim_section_2d_slider(clim)
    assert app_model.clim_2d == approx(clim)


def test_moving_clim_section_3d_slider_sets_the_apps_clim_3d(app_model, view_model):
    clim = (0.3, 0.9)
    view_model.move_clim_section_3d_slider(clim)
    assert app_model.clim_3d == approx(clim)


def test_setting_app_clim2d_updates_viewmodels_section_2d_slider(app_model, view_model: SidebarViewModel):
    clim = (0.4, 0.5)
    app_model.clim_2d = clim
    assert view_model.clim_section_2d == approx(clim)


def test_setting_app_clim3d_updates_viewmodels_section_3d_slider(app_model, view_model: SidebarViewModel):
    clim = (0.4, 0.5)
    app_model.clim_3d = clim
    assert view_model.clim_section_3d == approx(clim)
