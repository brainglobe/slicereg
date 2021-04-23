from unittest.mock import Mock

import numpy as np
import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.commands.utils import Signal
from slicereg.models.atlas import Atlas
from slicereg.models.transform_image import ImageTransformer
from slicereg.models.section import Section
from slicereg.repos.atlas_repo import AtlasRepo


@scenario("resample.feature", "Section Resample")
def test_impl():
    ...


@pytest.fixture
def repo():
    repo = Mock(BaseSectionRepo)
    repo.sections = [
        Section(image=ImageTransformer(channels=np.random.random((2, 3, 4))), pixel_resolution_um=20.)
    ]
    return repo


@pytest.fixture
def atlas_repo():
    repo = Mock(AtlasRepo)
    repo.get_atlas.return_value = Atlas(volume=np.random.random((5, 5, 5)), resolution_um=10)
    return repo

@pytest.fixture
def command(repo, atlas_repo):
    return ResampleSectionCommand(_repo=repo, _atlas_repo=atlas_repo, section_resampled=Mock(Signal))


@given("I have a 20um-resolution section loaded")
def step_impl(repo: BaseSectionRepo):
    assert len(repo.sections) == 1
    section = repo.sections[0]
    assert section.pixel_resolution_um == 20


@when("I set the resolution to 50um")
def step_impl(command: ResampleSectionCommand):
    command(resolution_um=50)
    

@then("I should see a 50um resolution slice onscreen")
def step_impl(command: ResampleSectionCommand):
    output = command.section_resampled.emit.call_args[1]
    assert output['resolution_um'] == 50
    assert 'section_image' in output
    assert output['transform'].shape == (4, 4)
