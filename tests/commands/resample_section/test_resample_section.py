from unittest.mock import Mock

import numpy as np
import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.commands.utils import Signal
from slicereg.models.image import Image
from slicereg.models.section import Section


@scenario("resample.feature", "Section Resample")
def test_impl():
    ...


@pytest.fixture
def repo():
    repo = Mock(BaseSectionRepo)
    repo.sections = [
        Section(image=Image(channels=np.random.random((2, 3, 4))), pixel_resolution_um=20.)
    ]
    return repo


@pytest.fixture
def command(repo):
    return ResampleSectionCommand(_repo=repo, section_resampled=Mock(Signal))


@given("I have a 20um-resolution section loaded")
def step_impl(repo: BaseSectionRepo):
    assert len(repo.sections) == 1
    section = repo.sections[0]
    assert section.image.pixel_resolution_um == 20


@when("I set the resolution to 50um")
def step_impl(command: ResampleSectionCommand):
    command(resolution_um=50)
    

@then("I should see a 50um resolution slice onscreen")
def step_impl(command: ResampleSectionCommand):
    output = command.section_resampled.emit.call_args[1]
    assert output['resolution_um'] == 50
    assert 'section_image' in output
    assert output['transform'].shape == (4, 4)

