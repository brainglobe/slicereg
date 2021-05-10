from dataclasses import dataclass, field
from typing import Tuple, List, Optional

import numpy as np
from numpy import ndarray

from slicereg.commands.utils import Signal
from slicereg.gui.commands import CommandProvider


@dataclass
class AppModel:
    _commands: CommandProvider
    updated: Signal = field(default_factory=Signal)
    window_title: str = "bg-slicereg"
    clim_2d: Tuple[float, float] = (0., 1.)
    clim_3d: Tuple[float, float] = (0., 1.)
    section_image: Optional[ndarray] = None
    section_image_resolution: Optional[float] = None
    section_transform: Optional[ndarray] = None
    atlas_image: Optional[ndarray] = None
    atlas_volume: ndarray = np.array([[[0]]], dtype=np.uint16)
    atlas_section_coords: Tuple[int, int, int] = (0, 0, 0)
    selected_ij: Tuple[int, int] = (0, 0)
    selected_xyz: Tuple[float, float, float] = (0, 0, 0)
    bgatlas_names: List[str] = field(default_factory=list)
    annotation_volume: Optional[np.ndarray] = None
    atlas_resolution: Optional[int] = None
    num_channels: Optional[int] = None
    current_channel: int = 1

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if hasattr(self, 'updated'):
            self.updated.emit(**{key: value})

    def _update_images(self,
                       atlas_image: Optional[ndarray] = None,
                       section_image: Optional[ndarray] = None,
                       section_transform: Optional[ndarray] = None,
                       section_image_resolution: Optional[float] = None,
                       num_channels: Optional[int] = None,
                       ):
        updates = {}
        if atlas_image is not None:
            self.atlas_image = atlas_image
            updates['atlas_image'] = atlas_image

        if section_image is not None:
            self.section_image = section_image
            updates['section_image'] = section_image

        if section_transform is not None:
            self.section_transform = section_transform
            updates['section_transform'] = section_transform

        if section_image_resolution is not None:
            self.section_image_resolution = section_image_resolution
            updates['section_image_resolution'] = section_image_resolution  # type: ignore

        if num_channels is not None:
            self.num_channels = num_channels
            self.current_channel = 1
            updates['num_channels'] = num_channels

        self.updated.emit(**updates)

    @property
    def clim_2d_values(self):
        return tuple(np.percentile(self.section_image, [self.clim_2d[0] * 100, self.clim_2d[1] * 100]))

    @property
    def clim_3d_values(self):
        return tuple(np.percentile(self.section_image, [self.clim_3d[0] * 100, self.clim_3d[1] * 100]))

    # Load Section
    def load_section(self, filename: str):
        result = self._commands.load_section(filename=filename)
        if result is not None:
            self._update_images(
                section_image=result.image,
                section_transform=result.transform,
                section_image_resolution=result.resolution_um,
                atlas_image=result.atlas_image,
                num_channels=result.num_channels,
            )

    # Select Channel
    def select_channel(self, num: int):
        result = self._commands.select_channel(channel=num)
        self.current_channel = result.current_channel
        self._update_images(section_image=result.section_image)

    # Resample Section
    def resample_section(self, resolution_um: float):
        self._commands.resample_section(resolution_um=resolution_um)

    def on_section_resampled(self, resolution_um: float, section_image: ndarray, transform: ndarray,
                             atlas_image: ndarray) -> None:
        self._update_images(atlas_image=atlas_image, section_image=section_image, section_transform=transform)

    # Move/Update Section Position/Rotation
    def move_section(self, **kwargs):
        results = self._commands.move_section(**kwargs)
        self._update_images(
            atlas_image=results.atlas_slice_image,
            section_transform=results.transform
        )

    def update_section(self, **kwargs):
        results = self._commands.update_section(**kwargs)
        self._update_images(
            atlas_image=results.atlas_slice_image,
            section_transform=results.transform
        )

    # Load Atlases
    def load_bgatlas(self, name: str):
        result = self._commands.load_atlas(bgatlas_name=name)
        self.atlas_volume = result.volume
        self.atlas_resolution = int(result.resolution)
        self.annotation_volume = result.annotation_volume

    def load_atlas_from_file(self, filename: str, resolution_um: int):
        result = self._commands.load_atlas_from_file(filename=filename, resolution_um=resolution_um)
        self.atlas_volume = result.volume
        self.atlas_resolution = int(result.resolution)
        x, y, z = tuple((np.array(self.atlas_volume.shape) * 0.5).astype(int).tolist())
        self.atlas_section_coords = x, y, z

    # List Brainglobe Atlases
    def list_bgatlases(self):
        results = self._commands.list_bgatlases()
        self.bgatlas_names = results.atlas_names

    # Get Physical Coordinate from Image Coordinate
    def select_coord(self, i: int, j: int):
        results = self._commands.get_atlas_coord(i=i, j=j)
        self.selected_ij = results.ij
        self.selected_xyz = results.xyz

    def _section_image(self, axis):
        if (volume := self.atlas_volume) is not None:
            section_slice_idx = self.atlas_section_coords[axis]
            return np.rollaxis(volume, axis)[section_slice_idx]
        else:
            return None

    @property
    def coronal_section_image(self):
        return self._section_image(axis=0)

    @property
    def axial_section_image(self):
        return self._section_image(axis=1)

    @property
    def sagittal_section_image(self):
        return  self._section_image(axis=2)