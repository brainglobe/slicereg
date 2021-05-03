from dataclasses import dataclass, field
from typing import Tuple, List

import numpy as np
from numpy import ndarray

from slicereg.commands.utils import Signal
from slicereg.gui.commands import CommandProvider

import typing as t


@dataclass
class AppModel:
    _commands: CommandProvider
    updated: Signal = field(default_factory=Signal)
    window_title: str = "bg-slicereg"
    clim_2d: Tuple[float, float] = (0., 1.)
    clim_3d: Tuple[float, float] = (0., 1.)
    _section_image: ndarray = np.array([[0]], dtype=np.uint16)
    section_transform: ndarray = np.eye(4)
    _atlas_image: ndarray = np.array([[0]], dtype=np.uint16)
    atlas_volume: ndarray = np.array([[[0]]], dtype=np.uint16)
    highlighted_image_coords: Tuple[int, int] = (0, 0)
    highlighted_physical_coords: Tuple[int, int, int] = (0, 0, 0)
    bgatlas_names: List[str] = field(default_factory=list)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if hasattr(self, 'updated'):
            self.updated.emit(**{key: value})

    # Load Section
    def load_section(self, filename: str):
        self._commands.load_section(filename=filename)

    def on_section_loaded(self, image: ndarray, atlas_image: ndarray, transform: ndarray, resolution_um: int) -> None:
        self._section_image = image
        self._atlas_image = atlas_image
        self.section_transform = transform

    # Select Channel
    def select_channel(self, num: int):
        self._commands.select_channel(channel=num)

    def on_channel_select(self, image: ndarray, channel: int) -> None:
        self._section_image = image

    # Resample Section
    def resample_section(self, resolution_um: float):
        self._commands.resample_section(resolution_um=resolution_um)

    def on_section_resampled(self, resolution_um: float, section_image: ndarray, transform: ndarray,
                             atlas_image: ndarray) -> None:
        self._section_image = section_image
        self._atlas_image = atlas_image
        self.section_transform = transform

    # Move/Update Section Position/Rotation
    def move_section(self, **kwargs):
        self._commands.move_section(**kwargs)

    def update_section(self, **kwargs):
        self._commands.update_section(**kwargs)

    def on_section_moved(self, transform: ndarray, atlas_slice_image: ndarray) -> None:
        self._atlas_image = atlas_slice_image
        self.section_transform = transform

    # Load Atlases
    def load_bgatlas(self, name: str):
        self._commands.load_atlas(bgatlas_name=name)

    def load_atlas_from_file(self, filename: str, resolution_um: int):
        self._commands.load_atlas_from_file(filename=filename, resolution_um=resolution_um)

    def on_atlas_update(self, volume: ndarray, transform: ndarray) -> None:
        self.atlas_volume = volume

    # List Brainglobe Atlases
    def list_bgatlases(self):
        self._commands.list_bgatlases()

    def on_bgatlas_list_update(self, atlas_names: t.List[str]) -> None:
        self.bgatlas_names = atlas_names

    # Get Physical Coordinate from Image Coordinate
    def get_coord(self, i: int, j: int):
        self._commands.get_coord(i=i, j=j)

    def on_image_coordinate_highlighted(self, image_coords, atlas_coords) -> None:
        i, j = image_coords
        self.highlighted_image_coords = (i, j)
        self.highlighted_physical_coords = atlas_coords