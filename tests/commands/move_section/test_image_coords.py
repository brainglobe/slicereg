from unittest.mock import Mock

import numpy as np
import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.get_coords import GetPixelRegistrationDataCommand
from slicereg.commands.utils import Signal
from slicereg.models.image import Image
from slicereg.models.section import Section


@scenario("section_affine_registration.feature", "Check Pixel Coordinate in Atlas Space")
def test_impl():
    ...


@pytest.fixture
def repo():
    repo = Mock(BaseSectionRepo)
    repo.sections = [
        Section(image=Image(channels=np.random.random((2, 3, 4)), pixel_resolution_um=12.))
    ]
    return repo


@pytest.fixture
def command(repo):
    return GetPixelRegistrationDataCommand(_repo=repo, coord_data_requested=Mock(Signal))


@given("I have loaded a section")
def step_impl(repo: BaseSectionRepo):
    assert len(repo.sections) == 1


@when("I indicate a section image coordinate")
def step_impl(command: GetPixelRegistrationDataCommand):
    command(i=2, j=1)


@then("the coordinate's 2D position and 3D position should appear")
def step_impl(command: GetPixelRegistrationDataCommand):
    output = command.coord_data_requested.emit.call_args[1]
    assert hasattr(output["image_coords"], "i")
    assert output['image_coords'].i == 2
    assert hasattr(output["image_coords"], "j")
    assert output['image_coords'].j == 1
    assert hasattr(output["atlas_coords"], "x")
    assert hasattr(output["atlas_coords"], "y")
    assert hasattr(output["atlas_coords"], "z")
