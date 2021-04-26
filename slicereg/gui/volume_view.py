from typing import Optional

import numpy as np
from PySide2.QtWidgets import QWidget
from numpy import array, ndarray
from vispy.app import KeyEvent, use_app
from vispy.scene import SceneCanvas, ViewBox, Volume, Image, ArcballCamera
from vispy.visuals import filters
from vispy.visuals.transforms import MatrixTransform

from slicereg.gui.base import BaseQtView
from slicereg.gui.commands import CommandProvider
from slicereg.gui.view_section import ViewSection


class VolumeView(BaseQtView):

    def __init__(self, commands: CommandProvider, view_section: ViewSection):

        self.commands = commands

        self.view_section = view_section
        self.view_section.clim_updated.connect(self.update_slice_image)

        self._canvas = SceneCanvas()

        self._viewbox = ViewBox(parent=self._canvas.scene)
        self._canvas.central_widget.add_widget(self._viewbox)
        self._viewbox.camera = ArcballCamera(fov=0)

        self._atlas_volume = Volume(array([[[1, 2]]]) * 1000, parent=self._viewbox.scene)  # , interpolation='nearest')
        self._atlas_volume.attach(filters.ColorFilter((1., .5, 0., 1.)))
        self._atlas_volume.set_gl_state('additive', depth_test=False)

        self._section_image = Image(parent=self._viewbox.scene, cmap='grays')
        self._section_image.attach(filters.ColorFilter((0., .5, 1., 1.)))
        self._section_image.set_gl_state('additive', depth_test=False)
        self._section_image_data: Optional[ndarray] = None

        self._canvas.events.key_press.connect(self._handle_vispy_key_press_events)

    def update_slice_image(self, image: Optional[ndarray] = None, transform: Optional[ndarray] = None):
        if image is not None:
            self._section_image.set_data(image.T)
            self._section_image_data = image.T

        if self._section_image_data is not None:
            self._section_image.clim = (np.percentile(self._section_image_data, self.view_section.clim[0] * 100),
                                        np.percentile(self._section_image_data, self.view_section.clim[1] * 100))
            if transform is not None:
                self._section_image.transform = MatrixTransform(transform.T)
            self._canvas.update()

    # View Code
    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def on_atlas_update(self, volume: ndarray, transform: ndarray):
        volume = volume.swapaxes(0, 2)
        self._atlas_volume.set_data(volume, clim=(np.min(volume), np.max(volume)))
        self._viewbox.camera.center = tuple(dim / 2 for dim in volume.shape)
        self._viewbox.camera.scale_factor = np.mean(volume.shape)
        self._canvas.update()

    def on_section_loaded(self, image: ndarray, atlas_image: ndarray, transform: Optional[ndarray], resolution_um: int):
        self.update_slice_image(image=image, transform=transform)

    def on_channel_select(self, image: ndarray, channel: int):
        self._section_image.set_data(image.T)
        self._section_image.clim = np.min(image), np.max(image)
        self._canvas.update()

    def on_section_moved(self, transform: ndarray, atlas_slice_image: ndarray):
        self._section_image.transform = MatrixTransform(transform.T)
        self._canvas.update()

    def on_section_resampled(self, resolution_um: float, section_image: ndarray, transform: ndarray, atlas_image: ndarray):
        self._section_image.set_data(section_image.T)
        self._section_image.transform = MatrixTransform(transform.T)
        self._canvas.update()

    # Controller Code
    def _handle_vispy_key_press_events(self, event: KeyEvent) -> None:
        """Router: Calls AppCommands functions based on the event that's given."""

        key_commands = {
            '1': lambda: self.commands.select_channel(1),
            '2': lambda: self.commands.select_channel(2),
            '3': lambda: self.commands.select_channel(3),
            '4': lambda: self.commands.select_channel(4),
            'W': lambda: self.commands.move_section(z=30),
            'S': lambda: self.commands.move_section(z=-30),
            'A': lambda: self.commands.move_section(x=-30),
            'D': lambda: self.commands.move_section(x=30),
            'Q': lambda: self.commands.move_section(y=-30),
            'E': lambda: self.commands.move_section(y=30),
            'I': lambda: self.commands.move_section(rz=3),
            'K': lambda: self.commands.move_section(rz=-3),
            'J': lambda: self.commands.move_section(rx=-3),
            'L': lambda: self.commands.move_section(rx=3),
            'U': lambda: self.commands.move_section(ry=-3),
            'O': lambda: self.commands.move_section(ry=3),
            'Escape': use_app().quit,
        }
        if command := key_commands.get(event.key.name):
            command()
