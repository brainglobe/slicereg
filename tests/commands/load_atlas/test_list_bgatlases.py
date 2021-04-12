from unittest.mock import Mock

import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.list_bgatlases import ListBgAtlasesCommand
from slicereg.commands.utils import Signal
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.repos.atlas_repo import AtlasRepo

@pytest.fixture
def reader():
    reader = Mock(BrainglobeAtlasReader)
    reader.list_available.return_value = ['awesome_atlas', 'super_atlas']
    return reader


@pytest.fixture
def command(reader):
    return ListBgAtlasesCommand(_reader=reader, atlas_list_updated=Mock(Signal))


@scenario("load_atlas.feature", "List Available Brainglobe Atlases")
def test_outlined():
    ...


@given("I am connected to the internet")
def step_impl(reader: BrainglobeAtlasReader):
    assert reader.list_available()


@when("I check brainglobe")
def step_impl(command: ListBgAtlasesCommand):
    command()


@then("I see a list of bg-atlasapi's available atlases.")
def step_impl(command: ListBgAtlasesCommand):
    view_model = command.atlas_list_updated.emit.call_args[1]
    assert view_model['atlas_names'] == ['awesome_atlas', 'super_atlas']
