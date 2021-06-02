import pytest
from unittest.mock import Mock

from vispy.scene.events import SceneMouseEvent

from slicereg.gui.app_model import AppModel
from slicereg.gui.atlas_section_window import AtlasSectionViewModel, AtlasSectionView
from slicereg.utils.introspection import get_public_attrs

@pytest.mark.gui
def test_slice_view_updates_without_error_for_all_viewmodel_fields(qtbot):
    for attr in get_public_attrs(AtlasSectionViewModel):
        model = AtlasSectionViewModel(_model=Mock(AppModel))
        view = AtlasSectionView(_model=model)
        qtbot.addWidget(view.qt_widget)
        setattr(model, attr, getattr(model, attr))  # set attribute with its own value

@pytest.mark.gui
def test_left_clicking_on_atlas_clice_view_triggers_left_mouse_click_on_viewmodel(qtbot):
    model = AtlasSectionViewModel(_model=Mock(AppModel))
    model.click_left_mouse_button = Mock()
    view = AtlasSectionView(_model=model)
    qtbot.addWidget(view.qt_widget)

    view.mouse_press(Mock(SceneMouseEvent, button=1, pos=(0, 0)))
    assert model.click_left_mouse_button.call_count == 1

@pytest.mark.gui
def test_left_dragging_on_atlas_clice_view_triggers_left_mouse_drag_on_viewmodel(qtbot):
    model = AtlasSectionViewModel(_model=Mock(AppModel))
    model.drag_left_mouse = Mock()
    view = AtlasSectionView(_model=model)
    qtbot.addWidget(view.qt_widget)

    view.mouse_move(
        Mock(SceneMouseEvent,
             press_event=Mock(SceneMouseEvent),
             button=1,
             pos=(0, 0),
             last_event=Mock(SceneMouseEvent, pos=(10, 10))
             )
    )
    assert model.drag_left_mouse.call_count == 1
