from unittest.mock import Mock

import numpy as np
import numpy.testing as npt

from slicereg.gui.app_model import AppModel
from slicereg.gui.slice_window import SliceViewModel
from slicereg.utils import DependencyInjector


def test_slice_viewmodel_displays_app_section_image():
    model = AppModel(_injector=Mock(DependencyInjector))
    view = SliceViewModel(_model=model)

    for _ in range(6):  # Run multiple iterations to check link
        image = np.random.randint(1, 10, size=(4, 4))
        model.section_image = image
        npt.assert_almost_equal(view.section_image, image)


def test_slice_viewmodel_displays_app_clim2d_values():
    model = AppModel(_injector=Mock(DependencyInjector))
    view = SliceViewModel(_model=model)

    for _ in range(6):  # Run multiple iterations to check link
        image = np.random.randint(1, 10, size=(4, 4))
        model.section_image = image
        model.clim_2d = (np.random.random() * 0.5, np.random.random() * 0.5 + 0.5)
        assert view.clim == model.clim_2d_values
