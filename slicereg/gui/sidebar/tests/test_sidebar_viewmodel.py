from unittest.mock import Mock

import pytest
from hypothesis import given
from hypothesis.strategies import floats, text
from pytest import approx

from slicereg.commands.constants import Plane
from slicereg.commands.move_section2 import ReorientRequest
from slicereg.gui.app_model import AppModel
from slicereg.gui.constants import VolumeType
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


cases = [
    ("click_coronal_button", Plane.Coronal),
    ("click_axial_button", Plane.Axial),
    ("click_sagittal_button", Plane.Sagittal),
]
@pytest.mark.parametrize("method_name,plane", cases)
def test_clicking_orientation_button_tells_app_to_rotate_slice_to_correct_orientation(method_name, plane):
    app_model = Mock(AppModel)
    view_model = SidebarViewModel(_model=app_model)
    getattr(view_model, method_name)()
    app_model.update_section.assert_called_with(ReorientRequest(plane=plane))


@pytest.mark.parametrize("clim", [(0.3, 0.8), (0.1, 0.3), (0.8, 0.82)])
def test_moving_clim_section_2d_slider_sets_the_apps_clim_2d(clim, app_model, view_model):
    view_model.move_clim_section_2d_slider(clim)
    assert app_model.clim_2d == approx(clim)


@pytest.mark.parametrize("clim", [(0.3, 0.8), (0.1, 0.3), (0.8, 0.82)])
def test_moving_clim_section_3d_slider_sets_the_apps_clim_3d(clim, app_model, view_model):
    view_model.move_clim_section_3d_slider(clim)
    assert app_model.clim_3d == approx(clim)


@pytest.mark.parametrize("clim", [(0.3, 0.8), (0.1, 0.3), (0.8, 0.82)])
def test_setting_app_clim2d_updates_viewmodels_section_2d_slider(clim, app_model, view_model: SidebarViewModel):
    app_model.clim_2d = clim
    assert view_model.clim_section_2d == approx(clim)


@pytest.mark.parametrize("clim", [(0.3, 0.8), (0.1, 0.3), (0.8, 0.82)])
def test_setting_app_clim3d_updates_viewmodels_section_3d_slider(clim, app_model, view_model: SidebarViewModel):
    app_model.clim_3d = clim
    assert view_model.clim_section_3d == approx(clim)


def test_clicking_quickload_button_calls_apps_load_section():
    app_model = Mock(AppModel)
    view_model = SidebarViewModel(_model=app_model)
    assert app_model.load_section.call_count == 0
    view_model.click_quick_load_section_button()
    assert app_model.load_section.call_count == 1


def test_clicking_load_section_button_calls_apps_load_section():
    app_model = Mock(AppModel)
    view_model = SidebarViewModel(_model=app_model)

    assert app_model.load_section.call_count == 0
    view_model.submit_load_section_from_file("myfile.tiff")
    assert app_model.load_section.call_count == 1
    assert app_model.load_section.called_with(filename="myfile.tiff")


def test_atlas_atlas_type_selector_buttons_selects_matching_volume(app_model, view_model):
    view_model.click_registration_atlas_selector_button()
    assert app_model.visible_volume == VolumeType.REGISTRATION

    view_model.click_annotation_atlas_selector_button()
    assert app_model.visible_volume == VolumeType.ANNOTATION

    view_model.click_registration_atlas_selector_button()
    assert app_model.visible_volume == VolumeType.REGISTRATION


@given(value=floats(-100, 100))
def test_appmodel_superior_attrs_update_sidebar_slider_values(app_model, view_model: SidebarViewModel, value):
    app_model.superior = value
    assert view_model.superior_slider_value == approx(value)


@given(value=floats(-100, 100))
def test_appmodel_anterior_attrs_update_sidebar_slider_values(app_model, view_model: SidebarViewModel, value):
    app_model.anterior = value
    assert view_model.anterior_slider_value == approx(value)


@given(value=floats(-100, 100))
def test_appmodel_right_attrs_update_sidebar_slider_values(app_model, view_model: SidebarViewModel, value):
    app_model.right = value
    assert view_model.right_slider_value == approx(value)


@given(value=floats(-100, 100))
def test_appmodel_rot_longitudinal_attrs_update_sidebar_slider_values(app_model, view_model: SidebarViewModel, value):
    app_model.rot_longitudinal = value
    assert view_model.rot_longitudinal_slider_value == approx(value)


@given(value=floats(-100, 100))
def test_appmodel_rot_anteroposterior_update_sidebar_slider_values(app_model, view_model: SidebarViewModel, value):
    app_model.rot_anteroposterior = value
    assert view_model.rot_anteroposterior_slider_value == approx(value)


@given(value=floats(-100, 100))
def test_appmodel_rot_horizontal_update_sidebar_slider_values(app_model, view_model: SidebarViewModel, value):
    app_model.rot_horizontal = value
    assert view_model.rot_horizontal_slider_value == approx(value)
