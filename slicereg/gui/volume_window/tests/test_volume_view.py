from unittest.mock import Mock

from slicereg.gui.app_model import AppModel
from slicereg.gui.volume_window import VolumeViewModel, VolumeView
from slicereg.utils.introspection import get_public_attrs


def test_volume_view_launches_without_errors(qtbot):
    view = VolumeView(VolumeViewModel(_model=Mock(AppModel)))
    qtbot.addWidget(view.qt_widget)


def test_slice_view_updates_without_error_for_all_viewmodel_fields(qtbot):
    for attr in get_public_attrs(VolumeViewModel):
        model = VolumeViewModel(_model=Mock(AppModel))
        view = VolumeView(_model=model)
        qtbot.addWidget(view.qt_widget)
        setattr(model, attr, getattr(model, attr))  # set attribute with its own value
