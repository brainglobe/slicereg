from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple, List, Optional

import numpy as np
from numpy import ndarray

from slicereg.commands.get_coords import MapImageCoordToAtlasCoordCommand
from slicereg.commands.list_atlases import ListRemoteAtlasesCommand
from slicereg.commands.load_atlas import LoadRemoteAtlasCommand, LoadAtlasFromFileCommand
from slicereg.commands.load_section import LoadSectionCommand
from slicereg.commands.move_section import MoveSectionCommand, UpdateSectionTransformCommand
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.utils.dependency_injector import DependencyInjector
from slicereg.utils.observable import HasObservableAttributes


class VolumeType(Enum):
    REGISTRATION = auto()
    ANNOTATION = auto()



@dataclass
class AppModel(HasObservableAttributes):
    _injector: DependencyInjector
    window_title: str = "bg-slicereg"
    clim_2d: Tuple[float, float] = (0., 1.)
    clim_3d: Tuple[float, float] = (0., 1.)
    section_image: Optional[ndarray] = None
    section_image_resolution: Optional[float] = None
    section_transform: Optional[ndarray] = None
    atlas_image: Optional[ndarray] = None
    registration_volume: ndarray = np.array([[[0]]], dtype=np.uint16)
    atlas_section_coords: Tuple[int, int, int] = (0, 0, 0)
    selected_ij: Tuple[int, int] = (0, 0)
    selected_xyz: Tuple[float, float, float] = (0, 0, 0)
    bgatlas_names: List[str] = field(default_factory=list)
    annotation_volume: Optional[np.ndarray] = None
    atlas_resolution: Optional[int] = None
    num_channels: Optional[int] = None
    current_channel: int = 1
    visible_volume: VolumeType = VolumeType.REGISTRATION

    def __post_init__(self):
        HasObservableAttributes.__init__(self)

    @property
    def clim_2d_values(self):
        return tuple(np.percentile(self.section_image, [self.clim_2d[0] * 100, self.clim_2d[1] * 100]))

    @property
    def clim_3d_values(self) -> Optional[Tuple[int, int]]:
        if self.section_image is not None:
            c_min, c_max = np.percentile(self.section_image, [self.clim_3d[0] * 100, self.clim_3d[1] * 100])
            return c_min, c_max
        else:
            return None

    # Load Section
    def load_section(self, filename: str):
        load_section = self._injector.build(LoadSectionCommand)
        result = load_section(filename=filename)
        if result is not None:
            self.section_image = result.image
            self.section_transform = result.transform
            self.section_image_resolution = result.resolution_um
            self.atlas_image = result.atlas_image
            self.num_channels = result.num_channels
            self.visible_volume = VolumeType.REGISTRATION

    # Select Channel
    def select_channel(self, num: int):
        select_channel = self._injector.build(SelectChannelCommand)
        result = select_channel(channel=num)
        self.current_channel = result.current_channel
        self.section_image = result.section_image

    # Resample Section
    def resample_section(self, resolution_um: float):
        resample_section = self._injector.build(ResampleSectionCommand)
        result = resample_section(resolution_um=resolution_um)
        self.atlas_image = result.atlas_image
        self.section_image = result.section_image
        self.section_transform = result.section_transform
        self.section_image_resolution = result.resolution_um

    # Move/Update Section Position/Rotation
    def move_section(self, **kwargs):
        move_section = self._injector.build(MoveSectionCommand)
        results = move_section(**kwargs)
        self.atlas_image = results.atlas_slice_image
        self.section_transform = results.transform

    def update_section(self, **kwargs):
        update_section = self._injector.build(UpdateSectionTransformCommand)
        results = update_section(**kwargs)
        self.atlas_image = results.atlas_slice_image
        self.section_transform = results.transform

    # Load Atlases
    def load_bgatlas(self, name: str):
        load_atlas = self._injector.build(LoadRemoteAtlasCommand)
        result = load_atlas(name=name)
        self.registration_volume = result.volume
        self.atlas_resolution = int(result.resolution)
        self.annotation_volume = result.annotation_volume

    def load_atlas_from_file(self, filename: str, resolution_um: int):
        load_atlas = self._injector.build(LoadAtlasFromFileCommand)
        result = load_atlas(filename=filename, resolution_um=resolution_um)
        self.registration_volume = result.volume
        self.atlas_resolution = int(result.resolution)
        x, y, z = tuple((np.array(self.registration_volume.shape) * 0.5).astype(int).tolist())
        self.atlas_section_coords = x, y, z

    # List Brainglobe Atlases
    def list_bgatlases(self):
        list_bgatlases = self._injector.build(ListRemoteAtlasesCommand)
        results = list_bgatlases()
        self.bgatlas_names = results.atlas_names

    # Get Physical Coordinate from Image Coordinate
    def select_coord(self, i: int, j: int):
        get_atlas_coord = self._injector.build(MapImageCoordToAtlasCoordCommand)
        results = get_atlas_coord(i=i, j=j)
        self.selected_ij = results.ij
        self.selected_xyz = results.xyz

    def _section_image(self, axis):
        if (volume := self.registration_volume) is not None:
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
        return self._section_image(axis=2)

    def press_key(self, key: str):
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
        }
        if command := key_commands.get(key):
            command()
