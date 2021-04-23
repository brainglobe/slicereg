from unittest.mock import Mock

import numpy as np
import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.commands.utils import Signal
from slicereg.models.section import Section
from slicereg.models.image import ImageTransformer


@pytest.fixture
def repo():
    repo = Mock(BaseSectionRepo)
    repo.sections = [
        Section(
            image=ImageTransformer(channels=np.arange(12).reshape(2, 3, 2)),
            pixel_resolution_um=12,
        )
    ]
    return repo

@pytest.fixture
def command(repo):
    return SelectChannelCommand(_repo=repo, channel_changed=Mock(Signal))


@scenario("multichannel.feature", "Switch Channels")
def test_impl():
    ...

@given("I have loaded an image with 2 channels")
def step_impl(repo):
    assert repo.sections[0].image.num_channels == 2


@when("I ask for channel 2")
def step_impl(command: SelectChannelCommand):
    command(channel=2)


@then("the onscreen section data changes to channel 2")
def step_impl(repo, command):
    output = command.channel_changed.emit.call_args[1]
    assert output['channel'] == 2
    assert np.all(np.isclose(output['image'], repo.sections[0].image.channels[1]))