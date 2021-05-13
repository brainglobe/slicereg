from unittest.mock import Mock

import pytest

from slicereg.app.app_model import AppModel
from slicereg.gui.volume_window.model import VolumeViewModel
import numpy as np

from slicereg.utils import DependencyInjector, Signal


@pytest.fixture
def view():
    MockAppModel = Mock(AppModel)
    return VolumeViewModel(_model=MockAppModel())


def test_key_press_w(view):
    view.press_key('W')
    view._model.move_section.assert_called_with(z=30)


def test_model_updated_clim():
    MockSignal = Mock(Signal)
    image = np.linspace(0, 10, num=10)[:, np.newaxis]
    model = AppModel(_injector=Mock(DependencyInjector), section_image=image)

    updated = MockSignal()
    view = VolumeViewModel(_model=model, updated=updated)
    clim = (0.1, 0.9)
    model.clim_3d = clim
    assert updated.emit.call_args[1]['changed'] == 'clim'
