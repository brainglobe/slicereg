import numpy as np
from numpy import array, ndarray
from PySide2.QtWidgets import QWidget
from vispy.app import KeyEvent, use_app
from vispy.scene import SceneCanvas, ViewBox, TurntableCamera, Volume, Image
from vispy.visuals import filters
from vispy.visuals.transforms import MatrixTransform

from slicereg.gui.base import BaseQtView


class VolumeView(BaseQtView):

    def __init__(self):

        self._canvas = SceneCanvas()

        self._viewbox = ViewBox(parent=self._canvas.scene)
        self._canvas.central_widget.add_widget(self._viewbox)
        self._viewbox.camera = TurntableCamera(fov=0, azimuth=0, elevation=90, distance=1000)

        self._atlas_volume = Volume(array([[[1, 2]]]) * 1000, parent=self._viewbox.scene, interpolation='nearest')
        self._atlas_volume.clim = (0., 1000.)
        self._atlas_volume.attach(filters.ColorFilter((1., .5, 0., 1.)))
        self._atlas_volume.set_gl_state('additive', depth_test=False)

        self._section_image = Image(parent=self._viewbox.scene, cmap='grays')
        self._section_image.attach(filters.ColorFilter((0., .5, 1., 1.)))
        self._section_image.set_gl_state('additive', depth_test=False)

        self._canvas.events.key_press.connect(self._handle_vispy_key_press_events)

    # View Code
    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def on_atlas_update(self, volume: ndarray, transform: ndarray):
        self._atlas_volume.set_data(volume)
        self._atlas_volume.transform = MatrixTransform(transform)
        self._atlas_volume.clim = np.min(volume), np.max(volume)
        self._viewbox.camera.center = (0, 0, 0)
        self._viewbox.camera.scale_factor = transform[0, 0] * volume.shape[0]
        self._canvas.update()

    def on_section_loaded(self, image: ndarray, transform: ndarray):
        self._section_image.set_data(image)
        self._section_image.clim = np.min(image), np.max(image)
        if transform is not None:
            self._section_image.transform = MatrixTransform(transform)
        self._canvas.update()

    def on_channel_select(self, image: ndarray, channel: int):
        self._section_image.set_data(image)
        self._section_image.clim = np.min(image), np.max(image)
        self._canvas.update()

    def on_section_moved(self, transform: ndarray):
        self._section_image.transform = MatrixTransform(transform)
        self._canvas.update()

    # Controller Code

    def _handle_vispy_key_press_events(self, event: KeyEvent) -> None:
        """Router: Calls AppCommands functions based on the event that's given."""

        key_commands = {
            '1': lambda: self.select_channel(1),
            '2': lambda: self.select_channel(2),
            '3': lambda: self.select_channel(3),
            '4': lambda: self.select_channel(4),
            'W': lambda: self.move_section(z=30),
            'S': lambda: self.move_section(z=-30),
            'A': lambda: self.move_section(x=-30),
            'D': lambda: self.move_section(x=30),
            'Q': lambda: self.move_section(y=-30),
            'E': lambda: self.move_section(y=30),
            'I': lambda: self.move_section(rz=3),
            'K': lambda: self.move_section(rz=-3),
            'J': lambda: self.move_section(rx=-3),
            'L': lambda: self.move_section(rx=3),
            'U': lambda: self.move_section(ry=-3),
            'O': lambda: self.move_section(ry=3),
            'Escape': use_app().quit,
        }
        if command := key_commands.get(event.key.name):
            command()

    def select_channel(self, num: int):
        raise NotImplementedError("Connect to a SelectChannelCommand before using")

    def move_section(self, x=0, y=0, z=0., rx=0., ry=0., rz=0.):
        raise NotImplementedError("Connect to MoveSectionCommand before using.")
