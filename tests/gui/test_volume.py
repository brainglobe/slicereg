from unittest.mock import Mock

import pytest

from slicereg.commands.utils import Signal
from slicereg.gui.commands import CommandProvider
from slicereg.gui.app_model import AppModel
from slicereg.gui.view_models.volume import VolumeViewModel
import numpy as np


@pytest.fixture
def view():
    MockAppModel = Mock(AppModel)
    return VolumeViewModel(_model=MockAppModel())


def test_key_press_w(view):
    view.on_key_press('W')
    view._model.move_section.assert_called_with(z=30)


def test_model_updated_clim():
    MockCommandProvider = Mock(CommandProvider)
    MockSignal = Mock(Signal)
    image = np.linspace(0, 10, num=10)[:, np.newaxis]
    model = AppModel(MockCommandProvider(), _section_image=image)

    updated = MockSignal()
    view = VolumeViewModel(_model=model, updated=updated)
    clim = (0.1, 0.9)
    model.clim_3d = clim
    assert updated.emit.call_args[1]['clim'] == (1., 9.)
