from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, List, Optional

import numpy as np
from numpy import ndarray
from result import Ok

from slicereg.commands.constants import Axis, Plane, Direction
from slicereg.commands.get_coords import MapImageCoordToAtlasCoordCommand
from slicereg.commands.list_atlases import ListRemoteAtlasesCommand
from slicereg.commands.load_atlas import LoadAtlasCommand, LoadBrainglobeAtlasRequest, LoadAtlasFromFileRequest
from slicereg.commands.load_section import LoadSectionCommand
from slicereg.commands.move_section2 import MoveSectionCommand2, MoveType, MoveRequest, ReorientRequest, CenterRequest, \
    ResampleRequest, UpdateSectionRequest, TranslateRequest, RotateRequest
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
        self._update_section(request=CenterRequest())

    # Select Channel
    def select_channel(self, num: int):
        select_channel = self._injector.build(SelectChannelCommand)
        result = select_channel(channel=num)
        if isinstance(result, Ok):
            data = result.value
            self.current_channel = data.current_channel
            self.section_image = data.section_image

    # Move/Update Section Position/Rotation/Orientation
    def update_section(self, **kwargs):
        axes = {'superior': Axis.Longitudinal, 'anterior': Axis.Anteroposterior, 'right': Axis.Horizontal,
                'rot_longitudinal': Axis.Longitudinal, 'rot_anteroposterior': Axis.Anteroposterior,
                'rot_horizontal': Axis.Horizontal}
        t, r = MoveType.TRANSLATION, MoveType.ROTATION
        move_types = {'superior': t, 'anterior': t, 'right': t, 'rot_longitudinal': r, 'rot_anteroposterior': r,
                      'rot_horizontal': r}
        for ax_name, value in kwargs.items():
            self._update_section(request=MoveRequest(axis=axes[ax_name], value=value, move_type=move_types[ax_name], absolute=True))

    def _update_section(self, request: UpdateSectionRequest):
        move_section = self._injector.build(MoveSectionCommand2)
        result = move_section(request=request)
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
            self.section_image = data.section_image
            self.section_image_resolution = data.resolution_um

    # Load Atlases
    def load_bgatlas(self, name: str):
        request = LoadBrainglobeAtlasRequest(name=name)
        command = self._injector.build(LoadAtlasCommand)
        result = command(request=request)
        if isinstance(result, Ok):
            data = result.value
            self.registration_volume = data.volume
            self.atlas_resolution = int(data.resolution)
            self.annotation_volume = data.annotation_volume

    def load_atlas_from_file(self, filename: str, resolution_um: int):
        load_atlas = self._injector.build(LoadAtlasCommand)
        request = LoadAtlasFromFileRequest(filename=filename, resolution_um=resolution_um)
        result = load_atlas(request)
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
            'W': lambda: self._update_section(TranslateRequest(direction=Direction.Anterior, value=30)),
            'S': lambda: self._update_section(TranslateRequest(direction=Direction.Posterior, value=30)),
            'A': lambda: self._update_section(TranslateRequest(direction=Direction.Left, value=30)),
            'D': lambda: self._update_section(TranslateRequest(direction=Direction.Right, value=30)),
            'Q': lambda: self._update_section(TranslateRequest(direction=Direction.Inferior, value=30)),
            'E': lambda: self._update_section(TranslateRequest(direction=Direction.Superior, value=30)),
            'I': lambda: self._update_section(RotateRequest(axis=Axis.Horizontal, value=5)),
            'K': lambda: self._update_section(RotateRequest(axis=Axis.Horizontal, value=-5)),
            'J': lambda: self._update_section(RotateRequest(axis=Axis.Longitudinal, value=5)),
            'L': lambda: self._update_section(RotateRequest(axis=Axis.Longitudinal, value=-5)),
            'U': lambda: self._update_section(RotateRequest(axis=Axis.Anteroposterior, value=-5)),
            'O': lambda: self._update_section(RotateRequest(axis=Axis.Anteroposterior, value=5)),
        }
        if command := key_commands.get(key):
            command()
