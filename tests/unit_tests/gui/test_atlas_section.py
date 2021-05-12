from unittest.mock import Mock

import pytest
import numpy as np
import numpy.testing as npt

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.gui.atlas_section_window.model import AtlasSectionViewModel


cases = [
    (0, 'coronal_section_image'),
    (1, 'axial_section_image'),
    (2, 'sagittal_section_image'),
]
@pytest.mark.parametrize("axis, section_attr", cases)
def test_app_model_coronal_section_is_the_first_axis_of_the_atlas_volume_and_at_the_first_atlas_section_coordinate(axis, section_attr):
    atlas_volume = np.random.randint(0, 100, (10, 10, 10), np.uint16)
    app_model = AppModel(_commands=Mock(CommandProvider), atlas_volume=atlas_volume)
    coronal_coord = app_model.atlas_section_coords[axis]
    npt.assert_equal(getattr(app_model, section_attr), np.rollaxis(atlas_volume, axis)[coronal_coord])


def test_coronal_section_view_model_displays_the_coronal_section_image():
    app_model = AppModel(
        _commands=Mock(CommandProvider),
        atlas_volume=np.random.randint(0, 100, (10, 10, 10), np.uint16)
    )
    view_model = AtlasSectionViewModel(axis=0, _model=app_model)
    npt.assert_equal(app_model.coronal_section_image, view_model.section_image)


def test_update_coords():
    model = AppModel(
        _commands=Mock(CommandProvider),
        atlas_volume=np.random.randint(0, 100, (10, 10, 10), np.uint16),
    )
    view_model = AtlasSectionViewModel(axis=0, _model=model, updated=Mock(Signal))
    model.atlas_section_coords = (1, 2, 3)
    result = view_model.updated.emit.call_args[1]['dto']
    npt.assert_equal(result.coords, (2, 3))
