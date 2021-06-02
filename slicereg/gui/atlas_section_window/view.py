from __future__ import annotations

from PySide2.QtWidgets import QWidget
from vispy.scene import SceneCanvas, ViewBox, TurntableCamera, Image, InfiniteLine
from vispy.scene.events import SceneMouseEvent
from vispy.visuals.transforms import MatrixTransform

from slicereg.gui.atlas_section_window import AtlasSectionViewModel
from slicereg.gui.base import BaseQtWidget


class AtlasSectionView(BaseQtWidget):

    def __init__(self, _model: AtlasSectionViewModel):
        self._model = _model
        self._model.register(self.update)

        self._canvas = SceneCanvas()

        self._viewbox = ViewBox(parent=self._canvas.scene)
        self._canvas.central_widget.add_widget(self._viewbox)

        self._viewbox.camera = TurntableCamera(
            interactive=False,
            fov=0,  # Makes it an ortho camera.
            azimuth=0,
            elevation=90,
        )

        self._slice = Image(cmap='grays', parent=self._viewbox.scene)
        self._slice.transform = MatrixTransform()
        self._slice.set_data(self._model.atlas_section_image)
        self._slice.clim = self._model.clim
        self._viewbox.camera.center = self._model.camera_center
        self._viewbox.camera.scale_factor = self._viewbox.camera.scale_factor

        self._vertical_line = InfiniteLine(pos=0, vertical=True, parent=self._viewbox.scene)
        self._horizontal_line = InfiniteLine(pos=0, vertical=False, parent=self._viewbox.scene)

        self._canvas.events.mouse_press.connect(self.mouse_press)
        self._canvas.events.mouse_move.connect(self.mouse_move)

        self._vertical_line.set_data(color=self._model.vertical_line_color)
        self._horizontal_line.set_data(color=self._model.horizontal_line_color)

    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def update(self, changed: str):
        render_funs = {
            'atlas_section_image': self._render_image,
            'plane': (lambda: None),
            'camera_scale': self._render_camera_scale,
            'camera_center': self._render_camera_center,
            'section_scale': self._render_section_scale,
            'horizontal_line_pos': self._render_horizontal_line,
            'vertical_line_pos': self._render_vertical_line,
        }
        render_funs[changed]()

    def mouse_press(self, event: SceneMouseEvent) -> None:
        event.handled = True

        # transform coordinates from canvas to image
        tr = self._canvas.scene.node_transform(self._viewbox.scene)
        assert len(event.pos) == 2
        x, y, _, _ = tr.map(event.pos)

        if event.button == 1:
            self._model.click_left_mouse_button(y=x, x=y)

    def mouse_move(self, event: SceneMouseEvent) -> None:
        if event.press_event is None:
            return

        # transform coordinates from canvas to image
        tr = self._canvas.scene.node_transform(self._viewbox.scene)
        x1, y1, _, _ = tr.map(event.last_event.pos)
        x2, y2, _, _ = tr.map(event.pos)

        if event.button == 1:  # Left Mouse Button
            self._model.drag_left_mouse(y1=int(x1), y2=int(x2), x1=int(y1), x2=int(y2))

    def _render_horizontal_line(self):
        self._vertical_line.set_data(pos=self._model.horizontal_line_pos)

    def _render_vertical_line(self):
        self._horizontal_line.set_data(pos=self._model.vertical_line_pos)

    def _render_image(self):
        self._slice.set_data(self._model.atlas_section_image)
        self._slice.clim = self._model.clim
        self._canvas.update()

    def _render_camera_scale(self):
        self._viewbox.camera.scale_factor = self._model.camera_scale
        self._canvas.update()

    def _render_camera_center(self):
        self._viewbox.camera.center = self._model.camera_center
        self._canvas.update()

    def _render_section_scale(self):
        self._slice.transform.reset()
        self._slice.transform.scale(self._model.section_scale)
        self._canvas.update()

