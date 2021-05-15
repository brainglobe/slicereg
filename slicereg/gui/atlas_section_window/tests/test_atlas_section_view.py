from unittest.mock import Mock

import pytest

from slicereg.app.app_model import AppModel
from slicereg.gui.atlas_section_window import AtlasSectionViewModel, AtlasSectionView
from slicereg.utils.introspection import get_public_attrs


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_slice_view_updates_without_error_for_all_viewmodel_fields(qtbot, axis):
    for attr in get_public_attrs(AtlasSectionViewModel):
        model = AtlasSectionViewModel(_model=Mock(AppModel), _axis=axis)
        view = AtlasSectionView(_model=model)
        qtbot.addWidget(view.qt_widget)
        setattr(model, attr, getattr(model, attr))  # set attribute with its own value
