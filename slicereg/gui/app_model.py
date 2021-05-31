from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, List, Optional

import numpy as np
from numpy import ndarray
from result import Ok, Err

from slicereg.commands.center_section import CenterSectionCommand
from slicereg.commands.get_coords import MapImageCoordToAtlasCoordCommand
from slicereg.commands.list_atlases import ListRemoteAtlasesCommand
from slicereg.commands.load_atlas import LoadRemoteAtlasCommand, LoadAtlasFromFileCommand
from slicereg.commands.load_section import LoadSectionCommand
from slicereg.commands.move_section2 import MoveSectionCommand2, Axis, MoveType
from slicereg.commands.register_section import RegisterSectionCommand
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.gui.constants import AtlasOrientation, VolumeType
from slicereg.utils.dependency_injector import DependencyInjector
from slicereg.utils.observable import HasObservableAttributes


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
    selected_xyz: Tuple[float, float, float] = (0, 0, 0)
    bgatlas_names: List[str] = field(default_factory=list)
    annotation_volume: Optional[np.ndarray] = None
    atlas_resolution: Optional[int] = None
    num_channels: Optional[int] = None
    current_channel: int = 1
    visible_volume: VolumeType = VolumeType.REGISTRATION
    x: float = 0.
    y: float = 0.
    z: float = 0.
    rx: float = 0.
    ry: float = 0.
    rz: float = 0.
    coronal_atlas_image: Optional[np.ndarray] = None
    axial_atlas_image: Optional[np.ndarray] = None
    sagittal_atlas_image: Optional[np.ndarray] = None

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
        if isinstance(result, Ok):
            data = result.value
            self.section_image = data.section_image
            self.section_image_resolution = data.resolution_um
            self.num_channels = data.num_channels
            self.visible_volume = VolumeType.REGISTRATION

        center_section = self._injector.build(CenterSectionCommand)
        result3 = center_section()
        if isinstance(result3, Ok):
            data3 = result3.value
            self.x = data3.x
            self.y = data3.y
            self.z = data3.z
            self.rx = data3.rx
            self.ry = data3.ry
            self.rz = data3.rz

        register_section = self._injector.build(RegisterSectionCommand)
        result2 = register_section()
        if isinstance(result2, Ok):
            data2 = result2.value
            self.atlas_image = data2.atlas_slice_image
            self.section_transform = data2.section_transform

    # Select Channel
    def select_channel(self, num: int):
        select_channel = self._injector.build(SelectChannelCommand)
        result = select_channel(channel=num)
        if isinstance(result, Ok):
            data = result.value
            self.current_channel = data.current_channel
            self.section_image = data.section_image

    # Resample Section
    def resample_section(self, resolution_um: float):
        resample_section = self._injector.build(ResampleSectionCommand)
        result = resample_section(resolution_um=resolution_um)
        if isinstance(result, Ok):
            data = result.value
            self.section_image = data.section_image
            self.section_image_resolution = data.resolution_um

        register_section = self._injector.build(RegisterSectionCommand)
        result2 = register_section()
        if isinstance(result2, Ok):
            data2 = result2.value
            self.atlas_image = data2.atlas_slice_image
            self.section_transform = data2.section_transform

    # Move/Update Section Position/Rotation
    def move_section(self, **kwargs):
        axes = {'x': Axis.X, 'y': Axis.Y, 'z': Axis.Z, 'rx': Axis.X, 'ry': Axis.Y, 'rz': Axis.Z}
        t, r = MoveType.TRANSLATION, MoveType.ROTATION
        move_types = {'x': t, 'y': t, 'z': t, 'rx': r, 'ry': r, 'rz': r}
        move_section = self._injector.build(MoveSectionCommand2)
        for ax_name, value in kwargs.items():
            result = move_section(axis=axes[ax_name], value=value, type=move_types[ax_name], absolute=False)
            if isinstance(result, Ok):
                data = result.value
                self.x = data.x
                self.y = data.y
                self.z = data.z
                self.rx = data.rx
                self.ry = data.ry
                self.rz = data.rz
            elif isinstance(result, Err):
                return

        register_section = self._injector.build(RegisterSectionCommand)
        result2 = register_section()
        if isinstance(result2, Ok):
            data2 = result2.value
            self.atlas_image = data2.atlas_slice_image
            self.section_transform = data2.section_transform

    def update_section(self, **kwargs):
        axes = {'x': Axis.X, 'y': Axis.Y, 'z': Axis.Z, 'rx': Axis.X, 'ry': Axis.Y, 'rz': Axis.Z}
        t, r = MoveType.TRANSLATION, MoveType.ROTATION
        move_types = {'x': t, 'y': t, 'z': t, 'rx': r, 'ry': r, 'rz': r}
        move_section = self._injector.build(MoveSectionCommand2)
        for ax_name, value in kwargs.items():
            result = move_section(axis=axes[ax_name], value=value, type=move_types[ax_name], absolute=True)
            if isinstance(result, Ok):
                data = result.value
                self.x = data.x
                self.y = data.y
                self.z = data.z
                self.rx = data.rx
                self.ry = data.ry
                self.rz = data.rz
            elif isinstance(result, Err):
                return

        register_section = self._injector.build(RegisterSectionCommand)
        result2 = register_section()
        if isinstance(result2, Ok):
            data2 = result2.value
            self.atlas_image = data2.atlas_slice_image
            self.section_transform = data2.section_transform
            self.coronal_atlas_image = data2.coronal_atlas_image
            self.axial_atlas_image = data2.axial_atlas_image
            self.sagittal_atlas_image = data2.sagittal_atlas_image

    # Load Atlases
    def load_bgatlas(self, name: str):
        load_atlas = self._injector.build(LoadRemoteAtlasCommand)
        result = load_atlas(name=name)
        if isinstance(result, Ok):
            data = result.value
            self.registration_volume = data.volume
            self.atlas_resolution = int(data.resolution)
            self.annotation_volume = data.annotation_volume
            self.x = data.atlas_center.x
            self.y = data.atlas_center.y
            self.z = data.atlas_center.z

    def load_atlas_from_file(self, filename: str, resolution_um: int):
        load_atlas = self._injector.build(LoadAtlasFromFileCommand)
        result = load_atlas(filename=filename, resolution_um=resolution_um)
        if isinstance(result, Ok):
            atlas = result.value
            self.registration_volume = atlas.volume
            self.atlas_resolution = int(atlas.resolution)

    # List Brainglobe Atlases
    def list_bgatlases(self):
        list_bgatlases = self._injector.build(ListRemoteAtlasesCommand)
        result = list_bgatlases()
        if isinstance(result, Ok):
            data = result.value
            self.bgatlas_names = data.atlas_names

    # Get Physical Coordinate from Image Coordinate
    def select_coord(self, i: int, j: int):
        get_atlas_coord = self._injector.build(MapImageCoordToAtlasCoordCommand)
        result = get_atlas_coord(i=i, j=j)
        if isinstance(result, Ok):
            data = result.value
            self.selected_xyz = data.xyz

    def orient_section_to(self, orientation: AtlasOrientation):
        if orientation is AtlasOrientation.CORONAL:
            self.update_section(rx=90, ry=0, rz=90)
        elif orientation is AtlasOrientation.AXIAL:
            self.update_section(rx=0, ry=90, rz=0)
        elif orientation is AtlasOrientation.SAGITTAL:
            self.update_section(rx=0, ry=180, rz=-90)

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
