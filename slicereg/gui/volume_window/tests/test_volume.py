from unittest.mock import Mock

import pytest

from slicereg.app.app_model import AppModel
from slicereg.gui.volume_window.viewmodel import VolumeViewModel


@pytest.fixture
def view():
    return VolumeViewModel(_model=Mock(AppModel))


def test_key_press_w(view):
    view.press_key('W')
    view._model.press_key.assert_called_with(key="W")
