from unittest.mock import Mock

import numpy as np
import pytest

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.gui.view_models.sidebar import SidebarViewModel


@pytest.fixture
def view_model():
    MockCommandProvider = Mock(CommandProvider)
    MockSignal = Mock(Signal)

    image = np.linspace(0, 10, num=10)[:, np.newaxis]
    model = AppModel(MockCommandProvider(), _section_image=image)
    updated = MockSignal()
    view = SidebarViewModel(_model=model, updated=updated)
    return view

def test_resolution_updated_with_section_text_change(view_model: SidebarViewModel):
    view_model.update_section_resolution_textbox('6.28')
    assert view_model._model.section_image_resolution==6.28