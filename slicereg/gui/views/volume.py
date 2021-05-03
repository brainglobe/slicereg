from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

import numpy as np
from PySide2.QtWidgets import QWidget
from numpy import array, ndarray
from vispy.app import KeyEvent, use_app
from vispy.scene import SceneCanvas, ViewBox, Volume, Image, ArcballCamera
from vispy.visuals import filters
from vispy.visuals.transforms import MatrixTransform

from slicereg.commands.utils import Signal
from slicereg.gui.model import AppModel
from slicereg.gui.views.base import BaseQtWidget, BaseViewModel, BaseView


class VolumeView(BaseQtWidget, BaseView):

    def __init__(self):
        super().__init__()
        self.model: Optional[VolumeViewModel] = None
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

        self._canvas.events.key_press.connect(self._handle_vispy_key_press_events)

    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def update(self, **kwargs) -> None:
        # if (volume := self.model.atlas_volume) is not None:
        # if dto.atlas_volume is not None:
        if (volume := kwargs.get('atlas_volume')) is not None:
            volume = volume.swapaxes(0, 2)
            self._atlas_volume.set_data(volume, clim=(np.min(volume), np.max(volume)))
            self._viewbox.camera.center = tuple(dim / 2 for dim in volume.shape)
            self._viewbox.camera.scale_factor = np.mean(volume.shape)

        if (image := kwargs.get('_section_image')) is not None:
            self._section_image.set_data(image.T)
            self._section_image.clim = (np.percentile(image, self.model.clim[0] * 100),
                                        np.percentile(image, self.model.clim[1] * 100))

        if (transform := kwargs.get('section_transform')) is not None:
            self._section_image.transform = MatrixTransform(transform.T)

        if (clim := kwargs.get('clim')) is not None:
            self._section_image.clim = (np.percentile(image, clim[0] * 100),
                                        np.percentile(image, clim[1] * 100))

        self._canvas.update()

    def _handle_vispy_key_press_events(self, event: KeyEvent) -> None:
        """Router: Calls AppCommands functions based on the event that's given."""
        if self.model is not None:
            self.model.on_key_press(event.key.name)


@dataclass(unsafe_hash=True)
class VolumeViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        print(self.__class__.__name__, f"updated {kwargs}")
        self.updated.emit(**kwargs)

    @property
    def clim(self) -> Tuple[float, float]:
        return self._model.clim_3d

    @clim.setter
    def clim(self, val):
        min, max = val
        self._model.clim_3d = (min, max)

    @property
    def atlas_volume(self) -> Optional[ndarray]:
        return self._model.atlas_volume

    @property
    def section_image(self) -> Optional[ndarray]:
        return self._model._section_image

    @property
    def section_transform(self) -> Optional[ndarray]:
        return self._model.section_transform

    def on_key_press(self, key: str):
        model = self._model
        key_commands = {
            '1': lambda: model.select_channel(1),
            '2': lambda: model.select_channel(2),
            '3': lambda: model.select_channel(3),
            '4': lambda: model.select_channel(4),
            'W': lambda: model.move_section(z=30),
            'S': lambda: model.move_section(z=-30),
            'A': lambda: model.move_section(x=-30),
            'D': lambda: model.move_section(x=30),
            'Q': lambda: model.move_section(y=-30),
            'E': lambda: model.move_section(y=30),
            'I': lambda: model.move_section(rz=3),
            'K': lambda: model.move_section(rz=-3),
            'J': lambda: model.move_section(rx=-3),
            'L': lambda: model.move_section(rx=3),
            'U': lambda: model.move_section(ry=-3),
            'O': lambda: model.move_section(ry=3),
            'Escape': use_app().quit,
        }
        if command := key_commands.get(key):
            command()
