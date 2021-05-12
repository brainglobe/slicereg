from __future__ import annotations

from PySide2.QtWidgets import QWidget
from vispy.scene import SceneCanvas, ViewBox, TurntableCamera, Image, InfiniteLine
from vispy.scene.events import SceneMouseEvent

from slicereg.gui.atlas_section_window.model import AtlasSectionDTO
from slicereg.gui.base import BaseQtWidget, BaseView


class AtlasSectionView(BaseQtWidget, BaseView):

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

        self._slice = Image(cmap='grays', parent=self._viewbox.scene)
        self._x_line = InfiniteLine(pos=0, vertical=False, parent=self._viewbox.scene)
        self._y_line = InfiniteLine(pos=0, vertical=True, parent=self._viewbox.scene)

    def on_registration(self, model):
        def _vispy_mouse_event(event: SceneMouseEvent) -> None:
            if event.type == 'mouse_press':
                event.handled = True

            elif event.type == 'mouse_move':
                if event.press_event is None:
                    return

                # transform coordinates from canvas to image
                tr = self._canvas.scene.node_transform(self._viewbox.scene)
                x1, y1, _, _ = tr.map(event.last_event.pos)
                x2, y2, _, _ = tr.map(event.pos)

                if event.button == 1:  # Left Mouse Button
                    model.on_left_mouse_drag(x1=int(x1), x2=int(x2), y1=int(y1), y2=int(y2))

        self._canvas.events.mouse_press.connect(_vispy_mouse_event)
        self._canvas.events.mouse_move.connect(_vispy_mouse_event)

        axis_colors = model.axis_colors
        self._x_line.set_data(color=axis_colors[0])
        self._y_line.set_data(color=axis_colors[1])

    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def update(self, dto):
        dto: AtlasSectionDTO

        if (image := dto.section_image) is not None:
            self._slice.set_data(image)
            self._slice.clim = 'auto'
            self._viewbox.camera.center = image.shape[1] / 2, image.shape[0] / 2, 0.
            self._viewbox.camera.scale_factor = max(image.shape)

        if (coords := dto.coords) is not None:
            self._x_line.set_data(pos=coords[0])
            self._y_line.set_data(pos=coords[1])

        self._canvas.update()
