from unittest.mock import Mock

import numpy as np
import pytest

from slicereg.app.app_model import AppModel
from slicereg.gui.sidebar.viewmodel import SidebarViewModel
from slicereg.utils import DependencyInjector


@pytest.fixture
def view_model():
    image = np.linspace(0, 10, num=10)[:, np.newaxis]
    model = AppModel(_injector=Mock(DependencyInjector), section_image=image)
    view = SidebarViewModel(_model=model)
    return view


def test_resolution_updated_with_section_text_change(view_model: SidebarViewModel):
    view_model.section_resolution_text = '6.28'
    assert view_model._model.section_image_resolution == 6.28
