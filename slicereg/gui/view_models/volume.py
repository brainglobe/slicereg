from dataclasses import dataclass, field

import numpy as np
from vispy.app import use_app

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel


@dataclass(unsafe_hash=True)
class VolumeViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        if (image := kwargs.get('section_image')) is not None:
            kwargs['section_image'] = image.T
            kwargs['clim'] = self._model.clim_3d_values
        if kwargs.get('clim_3d') is not None:
            kwargs['clim'] = self._model.clim_3d_values
        if (transform := kwargs.get('section_transform')) is not None:
            kwargs['section_transform'] = transform.T
        if (volume := kwargs.get('atlas_volume')) is not None:
            kwargs['camera_center'] = tuple(dim / 2 for dim in volume.shape)
            kwargs['camera_distance'] = np.mean(volume.shape)
            kwargs['volume_clim'] = (np.min(volume), np.max(volume))
            kwargs['atlas_volume'] = volume.swapaxes(0, 2)
        self.updated.emit(**kwargs)

    def press_key(self, key: str):
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
