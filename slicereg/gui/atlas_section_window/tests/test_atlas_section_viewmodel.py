from unittest.mock import Mock

import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import given
from hypothesis.strategies import sampled_from

from slicereg.gui.app_model import AppModel
from slicereg.gui.atlas_section_window.viewmodel import AtlasSectionViewModel
from slicereg.utils import DependencyInjector


@pytest.mark.parametrize("plane", ["coronal", "axial", "sagittal"])
def test_atlas_section_viewmodel_updates_atlas_section_image_to_match_cooresponding_coord(plane):
    app_model = AppModel(_injector=DependencyInjector(), x=2, y=5, z=10)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    section_image = np.random.randint(0, 100, (10, 10), np.uint16)
    setattr(app_model, f"{plane}_atlas_image", section_image)
    npt.assert_almost_equal(atlas_section_view.atlas_section_image, section_image)


def test_atlas_camera_center_and_scale_depend_on_the_atlas_shape_and_resolution():
    app_model = AppModel(
        _injector=DependencyInjector(),
        coronal_atlas_image=np.random.randint(0, 100, (10, 10), np.uint16),
    )
    atlas_section_view = AtlasSectionViewModel(plane='coronal', _model=app_model)
    atlas_section_view.section_scale


@given(plane=sampled_from(['coronal', 'sagittal', 'axial']))
def test_left_clicking_on_atlas_section_viewmodel_calls_position_setter_for_its_plane(plane):
    app_model = Mock(AppModel)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    atlas_section_view.click_left_mouse_button(x=0, y=0)
    assert app_model.update_section.call_count == 1


@given(plane=sampled_from(['coronal', 'sagittal', 'axial']))
def test_left_dragging_on_atlas_section_viewmodel_calls_position_setter_for_its_plane(plane):
    app_model = Mock(AppModel)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    atlas_section_view.drag_left_mouse(x1=0, y1=0, x2=10, y2=10)
    assert app_model.update_section.call_count == 1
