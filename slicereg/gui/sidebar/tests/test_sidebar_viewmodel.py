from functools import partial
from unittest.mock import Mock

import pytest
from hypothesis import given
from hypothesis.strategies import floats
from pytest import approx

from slicereg.app.app_model import AppModel
from slicereg.gui.sidebar.viewmodel import SidebarViewModel
from slicereg.utils import DependencyInjector

sensible_floats = partial(floats, allow_nan=False, allow_infinity=False)

@pytest.fixture(scope='module')
def app_model():
    app_model = AppModel(_injector=Mock(DependencyInjector))
    return app_model


@pytest.fixture(scope='module')
def view_model(app_model):
    return SidebarViewModel(_model=app_model)


@given(resolution=sensible_floats(0.01, 100))
def test_resolution_updated_with_section_text_change(resolution, view_model: SidebarViewModel):
    view_model.section_resolution_text = str(resolution)
    assert view_model._model.section_image_resolution == approx(resolution)


@given(resolution=sensible_floats(0.01, 100))
def test_viewmodel_resolution_updated_when_app_updates(resolution, view_model: SidebarViewModel, app_model):
    app_model.section_image_resolution = resolution
    assert view_model.section_resolution_text == str(resolution)


