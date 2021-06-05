from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, List, Optional

import numpy as np
from numpy import ndarray
from result import Ok, Err

from slicereg.commands.get_coords import MapImageCoordToAtlasCoordCommand
from slicereg.commands.list_atlases import ListRemoteAtlasesCommand
from slicereg.commands.load_atlas import LoadRemoteAtlasCommand, LoadAtlasFromFileCommand
from slicereg.commands.load_section import LoadSectionCommand
from slicereg.commands.move_section2 import MoveSectionCommand2, MoveType, MoveRequest, ReorientRequest, CenterRequest, \
    ResampleRequest
from slicereg.commands.constants import Axis, AtlasAxis
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
    superior: float = 0.
    anterior: float = 0.
    right: float = 0.
    rot_longitudinal: float = 0.
    rot_anteroposterior: float = 0.
    rot_horizontal: float = 0.
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

        move_section = self._injector.build(MoveSectionCommand2)
        result = move_section(CenterRequest())
        if isinstance(result, Ok):
            data = result.value
            self.superior = data.superior
            self.anterior = data.anterior
            self.right = data.right
            self.rot_longitudinal = data.rot_longitudinal
            self.rot_anteroposterior = data.rot_anteroposterior
            self.rot_horizontal = data.rot_horizontal
            self.atlas_image = data.atlas_slice_image
            self.section_transform = data.section_transform

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
        move_section = self._injector.build(MoveSectionCommand2)
        result = move_section(ResampleRequest(resolution_um=resolution_um))
        if isinstance(result, Ok):
            data = result.value
            self.section_image = data.section_image
            self.section_image_resolution = data.resolution_um
            self.atlas_image = data.atlas_slice_image
            self.section_transform = data.section_transform

    # Move/Update Section Position/Rotation/Orientation
    def update_section(self, absolute: bool = True, **kwargs):
        axes = {'superior': Axis.Longitudinal, 'anterior': Axis.Anteroposterior, 'right': Axis.Horizontal, 'rot_longitudinal': Axis.Longitudinal, 'rot_anteroposterior': Axis.Anteroposterior, 'rot_horizontal': Axis.Horizontal}
        t, r = MoveType.TRANSLATION, MoveType.ROTATION
        move_types = {'superior': t, 'anterior': t, 'right': t, 'rot_longitudinal': r, 'rot_anteroposterior': r, 'rot_horizontal': r}
        move_section = self._injector.build(MoveSectionCommand2)
        for ax_name, value in kwargs.items():
            if ax_name == 'orient':
                atlas_axes = {
                    AtlasOrientation.AXIAL: AtlasAxis.AXIAL,
                    AtlasOrientation.CORONAL: AtlasAxis.CORONAL,
                    AtlasOrientation.SAGITTAL: AtlasAxis.SAGITTAL,
                }
                axis = atlas_axes[value]
                reorient_request = ReorientRequest(axis=axis)
                result = move_section(request=reorient_request)
            else:
                move_request = MoveRequest(axis=axes[ax_name], value=value, move_type=move_types[ax_name], absolute=absolute)
                result = move_section(request=move_request)

            if isinstance(result, Ok):
                data = result.value
                self.superior = data.superior
                self.anterior = data.anterior
                self.right = data.right
                self.rot_longitudinal = data.rot_longitudinal
                self.rot_anteroposterior = data.rot_anteroposterior
                self.rot_horizontal = data.rot_horizontal
                self.atlas_image = data.atlas_slice_image
                self.section_transform = data.section_transform
                self.coronal_atlas_image = data.coronal_atlas_image
                self.axial_atlas_image = data.axial_atlas_image
                self.sagittal_atlas_image = data.sagittal_atlas_image

    # Load Atlases
    def load_bgatlas(self, name: str):
        load_atlas = self._injector.build(LoadRemoteAtlasCommand)
        result = load_atlas(name=name)
        if isinstance(result, Ok):
            data = result.value
            self.registration_volume = data.volume
            self.atlas_resolution = int(data.resolution)
            self.annotation_volume = data.annotation_volume
            self.superior = data.atlas_center.superior
            self.anterior = data.atlas_center.anterior
            self.right = data.atlas_center.right

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


    def press_key(self, key: str):
        key_commands = {
            '1': lambda: self.select_channel(1),
            '2': lambda: self.select_channel(2),
            '3': lambda: self.select_channel(3),
            '4': lambda: self.select_channel(4),
            'W': lambda: self.update_section(anterior=30, absolute=False),
            'S': lambda: self.update_section(anterior=-30, absolute=False),
            'A': lambda: self.update_section(right=-30, absolute=False),
            'D': lambda: self.update_section(right=30, absolute=False),
            'Q': lambda: self.update_section(superior=-30, absolute=False),
            'E': lambda: self.update_section(superior=30, absolute=False),
            'I': lambda: self.update_section(rot_horizontal=3, absolute=False),
            'K': lambda: self.update_section(rot_horizontal=-3, absolute=False),
            'J': lambda: self.update_section(rot_longitudinal=-3, absolute=False),
            'L': lambda: self.update_section(rot_longitudinal=3, absolute=False),
            'U': lambda: self.update_section(rot_anteroposterior=-3, absolute=False),
            'O': lambda: self.update_section(rot_anteroposterior=3, absolute=False),
        }
        if command := key_commands.get(key):
            command()
