from unittest.mock import Mock

import numpy as np
import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.commands.base import BaseImageReader
from slicereg.commands.load_atlas import LoadBrainglobeAtlasCommand
from slicereg.commands.load_section import BaseSectionRepo, LoadImageCommand
from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.io.tifffile import TiffImageReader
from slicereg.models.atlas import Atlas
from slicereg.models.image import Image
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def model():
    reader = Mock(BaseImageReader)
    reader.read.return_value = Image(channels=np.empty((2, 3, 2)), resolution_um=10)
    repo = Mock(BaseSectionRepo)
    repo.sections = []
    atlas_repo = AtlasRepo()
    commands = Mock(CommandProvider)
    commands.load_section = LoadImageCommand(_repo=repo, _atlas_repo=atlas_repo, _ome_reader=reader,
                                             _tiff_reader=Mock(TiffImageReader))
    reader = Mock(BrainglobeAtlasReader)
    reader.list_available.return_value = ['allen_mouse_25um']
    reader.read.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=25,
                                     annotation_volume=random.normal(size=(4, 4, 4)))
    commands.load_atlas = LoadBrainglobeAtlasCommand(_reader=reader, _repo=atlas_repo)
    model = AppModel(_commands=commands)
    model.load_bgatlas('test_atlas')
    return model


@scenario("load_slice.feature", "Single Slice Import")
def test_outlined():
    ...


@given("I have a multichannel OME-TIFF file on my computer.", target_fixture="filename")
def filename():
    return 'a_real_file.ome.tiff'


@given("No sections have been loaded yet")
def no_sections_loaded(model: AppModel):
    assert model.section_image is None
    assert model.atlas_image is None
    assert model.section_transform is None


@given("An atlas has been loaded")
def atlas_is_loaded(model: AppModel):
    assert model.atlas_volume is not None


@when("I load the file")
def load_file(model: AppModel, filename: str):
    model.load_section(filename=filename)


@then("I should see the slice image onscreen in 3D")
def check_for_loaded_3d_section(model: AppModel):
    assert model.section_image.ndim == 2
    assert model.section_transform.shape == (4, 4)


@then("I should see the atlas image onscreen in slice view")
def check_atlas_image_displayed(model: AppModel):
    assert model.atlas_image.ndim == 2


@then("The slice is centered on the image")
def check_the_transform_isnt_zero(model: AppModel):
    assert model.section_transform[0, -1] != 0
    assert model.section_transform[1, -1] != 0


@then("The displayed resolution is set to the image's resolution")
def check_resolution_is_sent(model: AppModel):
    assert model.section_image_resolution == 10
