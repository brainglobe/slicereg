from dataclasses import dataclass, field

import numpy as np
from numpy import ndarray

from slicereg.commands.utils import Signal
from slicereg.gui.commands import CommandProvider

import typing as t

from traitlets import HasTraits, Int, Tuple, Float, Unicode, List
from traittypes import Array

@dataclass()
class AppModel(HasTraits):
    _commands: CommandProvider
    updated: Signal = field(default_factory=Signal)
    window_title = Unicode("bg-slicereg")
    clim_2d = Tuple((0., 1.))
    clim_3d = Tuple((0., 1.))
    section_image = Array(np.array([[0]], dtype=np.uint16))
    section_transform = Array(np.eye(4))
    atlas_image = Array(np.array([[0]], dtype=np.uint16))
    atlas_volume = Array(np.array([[[0]]], dtype=np.uint16))
    highlighted_image_coords = Tuple((0, 0))
    highlighted_physical_coords = Tuple((0, 0, 0))
    bgatlas_names = List(Unicode())

    def update(self, **attrs):
        print(attrs)
        for attr, value in attrs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
            else:
                raise TypeError(f"Cannot set {attr}, {self.__class__.__name__} has no {attr} attribute.")
        self.updated.emit()

    # Load Section
    def load_section(self, filename: str):
        self._commands.load_section(filename=filename)

    def on_section_loaded(self, image: ndarray, atlas_image: ndarray, transform: ndarray, resolution_um: int) -> None:
        self.update(section_image=image, atlas_image=atlas_image, section_transform=transform)

    # Select Channel
    def select_channel(self, num: int):
        self._commands.select_channel(channel=num)

    def on_channel_select(self, image: ndarray, channel: int) -> None:
        self.update(section_image=image)

    # Resample Section
    def resample_section(self, resolution_um: float):
        self._commands.resample_section(resolution_um=resolution_um)

    def on_section_resampled(self, resolution_um: float, section_image: ndarray, transform: ndarray,
                             atlas_image: ndarray) -> None:
        self.update(section_image=section_image, atlas_image=atlas_image, section_transform=transform)

    # Move/Update Section Position/Rotation
    def move_section(self, **kwargs):
        self._commands.move_section(**kwargs)

    def update_section(self, **kwargs):
        self._commands.update_section(**kwargs)

    def on_section_moved(self, transform: ndarray, atlas_slice_image: ndarray) -> None:
        self.update(atlas_image=atlas_slice_image, section_transform=transform)


    # Load Atlases
    def load_bgatlas(self, name: str):
        self._commands.load_atlas(bgatlas_name=name)

    def load_atlas_from_file(self, filename: str, resolution_um: int):
        self._commands.load_atlas_from_file(filename=filename, resolution_um=resolution_um)

    def on_atlas_update(self, volume: ndarray, transform: ndarray) -> None:
        self.update(atlas_volume=volume)

    # List Brainglobe Atlases
    def list_bgatlases(self):
        self._commands.list_bgatlases()

    def on_bgatlas_list_update(self, atlas_names: t.List[str]) -> None:
        self.update(bgatlas_names=atlas_names)

    # Get Physical Coordinate from Image Coordinate
    def get_coord(self, i: int, j: int):
        self._commands.get_coord(i=i, j=j)

    def on_image_coordinate_highlighted(self, image_coords, atlas_coords) -> None:
        i, j = image_coords
        self.update(highlighted_image_coords=(i, j), highlighted_physical_coords=atlas_coords)