import numpy as np
from PySide2.QtWidgets import QWidget
from numpy import ndarray
from vispy.scene import SceneCanvas, ViewBox, TurntableCamera, Image
from vispy.scene.events import SceneMouseEvent
from vispy.visuals.filters import ColorFilter

from slicereg.gui.base import BaseQtView


class SliceView(BaseQtView):

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

    def on_section_loaded(self, image: ndarray, transform: ndarray) -> None:
        self.update_slice_image(image=image)

    def on_channel_select(self, image: ndarray, channel: int) -> None:
        self.update_slice_image(image=image)

    def on_section_moved(self, transform: ndarray, atlas_slice_image: ndarray) -> None:
        self.update_ref_slice_image(image=atlas_slice_image)

    def update_slice_image(self, image: ndarray):
        self._slice.set_data(image)
        self._slice.clim = np.min(image), np.max(image)
        self._viewbox.camera.center = image.shape[1] / 2, image.shape[0] / 2, 0.
        self._viewbox.camera.scale_factor = image.shape[1]
        self._canvas.update()

    def update_ref_slice_image(self, image: ndarray):
        self._reference_slice.set_data(image)
        self._reference_slice.clim = (np.min(image), np.max(image))  if np.max(image) - np.min(image) > 0 else (0, 1)
        self._canvas.update()

    def _vispy_mouse_event(self, event: SceneMouseEvent) -> None:
        if event.type == 'mouse_press':
            event.handled = True

        elif event.type == 'mouse_move':
            if event.press_event is None:
                return
            x1, y1 = event.last_event.pos
            x2, y2 = event.pos
            if event.button == 1:  # Left Mouse Button
                self._on_left_mouse_drag(x1=x1, y1=y1, x2=x2, y2=y2)
            elif event.button == 2:  # Right Mouse Button
                self._on_right_mouse_drag(x1=x1, y1=y1, x2=x2, y2=y2)

        elif event.type == 'mouse_wheel':
            self._on_mousewheel_move(increment=int(event.delta[1]))


    def _on_left_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        x_amp = abs(x2 - x1)
        y_amp = abs(y2 - y1)
        x_dir = ((x2 > x1) * 2) - 1
        y_dir = ((y2 > y1) * 2) - 1
        scale = 4.
        x_slice_offset = x_amp * x_dir * scale
        y_slice_offset = y_amp * y_dir * scale
        self.move_section(x=x_slice_offset, y=y_slice_offset)
        self.get_coord_data(i=0, j=0)  # todo: replace with mouse highlighting

    def _on_right_mouse_drag(self, x1: int, y1: int, x2: int, y2: int):
        x_amp = abs(x2 - x1)
        x_dir = ((x2 > x1) * 2) - 1
        scale = .1
        x_slice_offset = x_amp * x_dir * scale
        self.move_section(ry=x_slice_offset)

    def _on_mousewheel_move(self, increment: int):
        self.move_section(z=10 * increment)

    def move_section(self, right=0., superior=0., anterior=0., rot_lateral=0., rot_axial=0., rot_median=0.) -> None:
        raise NotImplementedError("Wire up to MoveSectionCommand to use this.")

    def get_coord_data(self, i: int, j: int):
        raise NotImplementedError("Wire up to GetPixelRegistrationDataCommand to use this.")

    def on_section_resampled(self, resolution_um: float, section_image: ndarray, transform: ndarray):
        self.update_slice_image(image=section_image)