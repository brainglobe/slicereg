from unittest.mock import Mock

import numpy as np
import pytest

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.gui.view_models.slice import SliceViewModel


@pytest.fixture
def view_model():
    MockCommandProvider = Mock(CommandProvider)
    MockSignal = Mock(Signal)

    image = np.linspace(0, 10, num=10)[:, np.newaxis]
    model = AppModel(MockCommandProvider(), _section_image=image)
    updated = MockSignal()
    view = SliceViewModel(_model=model, updated=updated)
    return view


def test_model_updated_clim(view_model: SliceViewModel):
    clim = (0.1, 0.9)
    view_model._model.clim_2d = clim
    args, kwargs = view_model.updated.emit.call_args
    assert kwargs['dto'].clim == (1., 9.)
