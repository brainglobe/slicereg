from __future__ import annotations

from dataclasses import field, dataclass
from typing import Optional, Tuple

import numpy as np
from PySide2.QtWidgets import QWidget
from numpy import ndarray
from vispy.scene import SceneCanvas, ViewBox, TurntableCamera, Image
from vispy.scene.events import SceneMouseEvent
from vispy.visuals.filters import ColorFilter

from slicereg.commands.utils import Signal
from slicereg.gui.commands import CommandProvider
from slicereg.gui.model import AppModel
from slicereg.gui.views.base import BaseQtWidget, BaseView, BaseViewModel


class SliceView(BaseQtWidget, BaseView):

    def __init__(self):

        self.model: Optional[SliceViewModel] = None

        self._canvas = SceneCanvas()

        self._viewbox = ViewBox(parent=self._canvas.scene)
        self._canvas.central_widget.add_widget(self._viewbox)

        self._viewbox.camera = TurntableCamera(
            interactive=False,
            fov=0,  # Makes it an ortho camera.
            azimuth=0,
            elevation=-90,
        )

        self._reference_slice = Image(cmap='grays', parent=self._viewbox.scene)
        self._reference_slice.attach(ColorFilter((1., .5, 0., 1.)))
        self._reference_slice.set_gl_state('additive', depth_test=False)

        self._slice = Image(cmap='grays', parent=self._viewbox.scene)
        self._slice.attach(ColorFilter((0., .5, 1., 1.)))
        self._slice.set_gl_state('additive', depth_test=False)

        self._canvas.events.mouse_press.connect(self._vispy_mouse_event)
        self._canvas.events.mouse_move.connect(self._vispy_mouse_event)
        self._canvas.events.mouse_release.connect(self._vispy_mouse_event)
        self._canvas.events.mouse_wheel.connect(self._vispy_mouse_event)

    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def register_viewmodel(self, model: SliceViewModel) -> None:
        self.model = model
        self.model.updated.connect(self.update)

    def update(self, model: SliceViewModel):
        if (image := model.section_image) is not None:
            self._slice.set_data(image)
            self._slice.clim = (np.percentile(image, model.clim[0] * 100), np.percentile(image, model.clim[1] * 100))
            self._viewbox.camera.center = image.shape[1] / 2, image.shape[0] / 2, 0.
            self._viewbox.camera.scale_factor = image.shape[1]

        if (image := model.atlas_image) is not None:
            self._reference_slice.set_data(image)
            self._reference_slice.clim = (np.min(image), np.max(image)) if np.max(image) - np.min(image) > 0 else (0, 1)

        self._canvas.update()

    def _vispy_mouse_event(self, event: SceneMouseEvent) -> None:
        if self.model:
            if event.type == 'mouse_press':
                event.handled = True

            elif event.type == 'mouse_move':
                if event.press_event is None:
                    return
                x1, y1 = event.last_event.pos
                x2, y2 = event.pos
                if event.button == 1:  # Left Mouse Button
                    self.model.on_left_mouse_drag(x1=x1, x2=x2, y1=y1, y2=y2)
                elif event.button == 2:  # Right Mouse Button
                    self.model.on_right_mouse_drag(x1=x1, y1=y1, x2=x2, y2=y2)

            elif event.type == 'mouse_wheel':
                self.model.on_mousewheel_move(increment=int(event.delta[1]))





@dataclass
class SliceViewModel(BaseViewModel):
    _model: AppModel = field(repr=False)
    _commands: CommandProvider = field(repr=False)
    updated: Signal = field(default_factory=Signal, repr=False)

    def __post_init__(self):
        self._model.updated.connect(self.update)
        self.update()

    def register_view(self, view: BaseView):
        view.register_viewmodel(model=self)

    def update(self):
        self.updated.emit(model=self)

    @property
    def clim(self) -> Tuple[float, float]:
        return self._model.clim_2d

    @clim.setter
    def clim(self, val):
        self._model.update(clim_2d=val)

    @property
    def section_image(self) -> Optional[ndarray]:
        return self._model.section_image

    @property
    def atlas_image(self) -> Optional[ndarray]:
        return self._model.atlas_image

    def on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        scale = 4.
        scaled_dx = (x2 - x1) * scale
        scaled_dy = (y2 - y1) * scale
        self._commands.move_section(x=scaled_dx, z=scaled_dy)
        self._commands.get_coord(i=x2, j=y2)

    def on_right_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        scale = 1.
        scaled_dx = (x2 - x1) * scale
        scaled_dy = (y2 - y1) * scale
        self._commands.move_section(rx=scaled_dx, rz=scaled_dy)

    def on_mousewheel_move(self, increment: int):
        scale = 10
        self._commands.move_section(y=scale * increment)
