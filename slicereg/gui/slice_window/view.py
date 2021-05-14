from __future__ import annotations

import numpy as np
from PySide2.QtWidgets import QWidget
from vispy.scene import SceneCanvas, ViewBox, TurntableCamera, Image
from vispy.scene.events import SceneMouseEvent
from vispy.visuals.filters import ColorFilter

from slicereg.gui.base import BaseQtWidget
from slicereg.gui.slice_window.viewmodel import SliceViewModel


class SliceView(BaseQtWidget):

    def __init__(self, _model: SliceViewModel):
        self._model = _model
        self._model.register(self.update)

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

        self._canvas.events.mouse_press.connect(self.mouse_press)
        self._canvas.events.mouse_move.connect(self.mouse_move)
        self._canvas.events.mouse_wheel.connect(self.mouse_wheel)

    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def mouse_press(self, event: SceneMouseEvent) -> None:
        event.handled = True

    def mouse_move(self, event: SceneMouseEvent) -> None:
        if event.press_event is None:
            return
        x1, y1 = event.last_event.pos
        x2, y2 = event.pos
        if event.button == 1:  # Left Mouse Button
            self._model.on_left_mouse_drag(x1=x1, x2=x2, y1=y1, y2=y2)
        elif event.button == 2:  # Right Mouse Button
            self._model.on_right_mouse_drag(x1=x1, y1=y1, x2=x2, y2=y2)

    def mouse_wheel(self, event: SceneMouseEvent):
        self._model.on_mousewheel_move(increment=int(event.delta[1]))

    def update(self, changed: str) -> None:
        render_funs = {
            'section_image': self._render_section_image,
            'clim': self._render_section_clim,
            'atlas_image': self._render_atlas_image,
        }
        render_funs[changed]()

    def _render_atlas_image(self):
        image = self._model.atlas_image
        self._reference_slice.set_data(image)
        self._reference_slice.clim = (np.min(image), np.max(image)) if np.max(image) - np.min(image) > 0 else (0, 1)
        self._canvas.update()

    def _render_section_clim(self):
        self._slice.clim = self._model.clim
        self._canvas.update()

    def _render_section_image(self):
        image = self._model.section_image
        self._slice.set_data(image)
        self._viewbox.camera.center = image.shape[1] / 2, image.shape[0] / 2, 0.
        self._viewbox.camera.scale_factor = image.shape[1]
        self._canvas.update()
