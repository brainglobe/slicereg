from unittest.mock import Mock

import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.move_section import MoveSectionCommand
from slicereg.commands.utils import Signal
from slicereg.models.section import Section
from slicereg.models.image import ImagePlane, SliceImage


@scenario("section_affine_registration.feature", "Move Section in 3D")
def test_impl():
    ...


@pytest.fixture
def repo():
    repo = Mock(BaseSectionRepo)
    repo.sections = [
        Section(image=Mock(SliceImage, pixel_resolution_um=12), plane=ImagePlane(0, 0))
    ]
    return repo


@pytest.fixture
def command(repo):
    return MoveSectionCommand(_repo=repo, section_moved=Mock(Signal))


@given("I have loaded a section")
def step_impl(repo: BaseSectionRepo):
    assert len(repo.sections) == 1


@when("I ask for the section to be translated and rotated")
def step_impl(command: MoveSectionCommand):
    command(x=2, y=5, z=10, rx=90, ry=0, rz=10)


@then("the image is updated with a new 3D transform")
def step_impl(command: MoveSectionCommand):
    output = command.section_moved.emit.call_args[1]
    assert 'transform' in output
    assert output['transform'].shape == (4, 4)
