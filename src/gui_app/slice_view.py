import numpy as np
from PySide2.QtWidgets import QWidget
from numpy import ndarray
from vispy.scene import SceneCanvas, ViewBox, TurntableCamera, Image
from vispy.scene.events import SceneMouseEvent
from vispy.visuals.filters import ColorFilter

from src.gui_app.base import BaseVispyView
from src.use_cases.provider import UseCaseProvider


class SliceView(BaseVispyView):

    def __init__(self):
        self._canvas = SceneCanvas()

        self._viewbox = ViewBox(parent=self._canvas.scene)
        self._canvas.central_widget.add_widget(self._viewbox)

        self._viewbox.camera = TurntableCamera(
            interactive=False,
            fov=0,  # Makes it an ortho camera.
            azimuth=0,
            elevation=-90,
        )

        self._reference_slice = Image(
            cmap='grays',
            parent=self._viewbox.scene
        )
        self._reference_slice.attach(ColorFilter((1., .5, 0., 1.)))
        self._reference_slice.set_gl_state('additive', depth_test=False)

        self._slice = Image(
            cmap='grays',
            parent=self._viewbox.scene
        )
        self._slice.attach(ColorFilter((0., .5, 1., 1.)))
        self._slice.set_gl_state('additive', depth_test=False)

    def register_use_cases(self, app: UseCaseProvider):
        self.use_cases = app

        self._canvas.events.mouse_press.connect(self._vispy_mouse_event)
        self._canvas.events.mouse_move.connect(self._vispy_mouse_event)
        self._canvas.events.mouse_release.connect(self._vispy_mouse_event)

    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def update_slice_image(self, image: ndarray):
        self._slice.set_data(image)
        self._slice.clim = np.min(image), np.max(image)
        self._canvas.update()

    def show_new_slice(self, slice: ndarray, ref_slice: ndarray):
        self._viewbox.camera.center = ref_slice.shape[1] / 2, ref_slice.shape[0] / 2, 0.
        self._viewbox.camera.scale_factor = ref_slice.shape[1]
        self._reference_slice.set_data(ref_slice)
        self._reference_slice.clim = np.min(ref_slice), np.max(ref_slice)
        self._viewbox.camera.scale_factor = slice.shape[1]
        self._slice.set_data(slice)
        self._slice.clim = np.min(slice), np.max(slice)
        self._canvas.update()

    def _vispy_mouse_event(self, event: SceneMouseEvent) -> None:
        if event.type == 'mouse_press':
            event.handled = True
            return

        elif event.type == 'mouse_move':
            if event.press_event is None:
                return
            x1, y1 = event.last_event.pos
            x2, y2 = event.pos
            if event.button == 1:  # Left Mouse Button
                self._on_left_mouse_drag(x1=x1, y1=y1, x2=x2, y2=y2)
            elif event.button == 2:  # Right Mouse Button
                self._on_right_mouse_drag(x1=x1, y1=y1, x2=x2, y2=y2)

    def _on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        x_amp = abs(x2 - x1)
        y_amp = abs(y2 - y1)
        x_dir = ((x2 > x1) * 2) - 1
        y_dir = ((y2 > y1) * 2) - 1
        scale = 4.
        x_slice_offset = x_amp * x_dir * scale
        y_slice_offset = y_amp * y_dir * scale
        self.use_cases.move_section(x=x_slice_offset, y=y_slice_offset)

    def _on_right_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        x_amp = abs(x2 - x1)
        x_dir = ((x2 > x1) * 2) - 1
        scale = .1
        x_slice_offset = x_amp * x_dir * scale
        self.use_cases.move_section(ry=x_slice_offset)
