from unittest.mock import Mock

import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import given
from hypothesis.strategies import floats, sampled_from

from slicereg.gui.app_model import AppModel
from slicereg.gui.atlas_section_window.viewmodel import AtlasSectionViewModel
from slicereg.utils import DependencyInjector

cases = [
    (0, 'coronal_section_image'),
    (1, 'axial_section_image'),
    (2, 'sagittal_section_image'),
]


@pytest.mark.parametrize("axis, section_attr", cases)
def test_app_model_coronal_section_is_the_first_axis_of_the_atlas_volume_and_at_the_first_atlas_section_coordinate(axis,
                                                                                                                   section_attr):
    atlas_volume = np.random.randint(0, 100, (10, 10, 10), np.uint16)
    app_model = AppModel(_injector=Mock(DependencyInjector), registration_volume=atlas_volume)
    coronal_coord = app_model.atlas_section_coords[axis]
    npt.assert_equal(getattr(app_model, section_attr), np.rollaxis(atlas_volume, axis)[coronal_coord])


@given(value=floats(-50, 50), attributes=sampled_from([('coronal', 'x'), ('axial', 'y'), ('sagittal', 'z')]))
def test_atlas_section_viewmodel_updates_depth_on_app_model_coord_change(value, attributes):
    plane, coord_name = attributes
    app_model = AppModel(_injector=DependencyInjector(), x=0, y=0, z=0)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    setattr(app_model, coord_name, value)

    assert atlas_section_view.image_coords == (0, 0)
    assert atlas_section_view.depth == value


@given(
    value=floats(-50, 50),
    attrs=sampled_from(
        [('coronal', 'coronal_image_coords'),
         ('axial', 'axial_image_coords'),
         ('sagittal', 'sagittal_image_coords')
         ]
    ),
    coord=sampled_from(['x', 'y', 'z'])
)
def test_atlas_section_viewmodel_updates_image_coords_to_corresponding_appmodel_image_coords_on_app_model_coord_change(
        value, attrs, coord):
    plane, coord_attr = attrs
    app_model = AppModel(_injector=Mock(DependencyInjector), x=2, y=5, z=10)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    setattr(app_model, coord, value)
    assert atlas_section_view.image_coords == getattr(app_model, coord_attr)


@pytest.mark.parametrize("plane", ["coronal", "axial", "sagittal"])
def test_atlas_section_viewmodel_updates_atlas_section_image_to_match_cooresponding_coord(plane):
    app_model = AppModel(_injector=DependencyInjector(), x=2, y=5, z=10)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    app_model.x = 10
    section_image = getattr(app_model, f"{plane}_section_image")
    npt.assert_almost_equal(atlas_section_view.atlas_section_image, section_image)


@given(plane=sampled_from(['coronal', 'sagittal', 'axial']))
def test_left_clicking_on_atlas_section_viewmodel_calls_position_setter_for_its_plane(plane):
    app_model = Mock(AppModel)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    atlas_section_view.click_left_mouse_button(x=0, y=0)
    kwargs = app_model.set_pos_to_plane_indices.call_args[1]
    assert kwargs['plane'] == plane
    assert isinstance(kwargs['i'], int) and isinstance(kwargs['j'], int)


@given(plane=sampled_from(['coronal', 'sagittal', 'axial']))
def test_left_dragging_on_atlas_section_viewmodel_calls_position_setter_for_its_plane(plane):
    app_model = Mock(AppModel)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    atlas_section_view.drag_left_mouse(x1=0, y1=0, x2=10, y2=10)
    kwargs = app_model.set_pos_to_plane_indices.call_args[1]
    assert kwargs['plane'] == plane
    assert isinstance(kwargs['i'], int) and isinstance(kwargs['j'], int)
