from __future__ import annotations

from dataclasses import dataclass

from slicereg.commands.base import BaseRepo, BaseRemoteAtlasReader, BaseLocalAtlasReader, BaseLocalImageReader
from slicereg.commands.get_coords import MapImageCoordToAtlasCoordCommand
from slicereg.commands.list_atlases import ListRemoteAtlasesCommand
from slicereg.commands.load_atlas import LoadRemoteAtlasCommand, LoadAtlasFromFileCommand
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand, UpdateSectionTransformCommand
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand


@dataclass(frozen=True)
class CommandBuilder:
    _repo: BaseRepo
    _remote_atlas_reader: BaseRemoteAtlasReader
    _local_atlas_reader: BaseLocalAtlasReader
    _image_reader: BaseLocalImageReader


    @property
    def load_atlas(self) -> LoadRemoteAtlasCommand:
        return LoadRemoteAtlasCommand(_repo=self._repo, _remote_atlas_reader=self._remote_atlas_reader)

    @property
    def load_section(self) -> LoadImageCommand:
        return LoadImageCommand(
            _repo=self._repo,
            _image_reader=self._image_reader,
        )

    @property
    def load_atlas_from_file(self) -> LoadAtlasFromFileCommand:
        return LoadAtlasFromFileCommand(_repo=self._repo, _local_atlas_reader=self._local_atlas_reader)

    @property
    def list_bgatlases(self) -> ListRemoteAtlasesCommand:
        return ListRemoteAtlasesCommand(_remote_atlas_reader=self._remote_atlas_reader)

    @property
    def select_channel(self) -> SelectChannelCommand:
        return SelectChannelCommand(_repo=self._repo)

    @property
    def move_section(self) -> MoveSectionCommand:
        return MoveSectionCommand(_repo=self._repo)

    @property
    def update_section(self) -> UpdateSectionTransformCommand:
        return UpdateSectionTransformCommand(_repo=self._repo)

    @property
    def get_atlas_coord(self) -> MapImageCoordToAtlasCoordCommand:
        return MapImageCoordToAtlasCoordCommand(_repo=self._repo)

    @property
    def resample_section(self) -> ResampleSectionCommand:
        return ResampleSectionCommand(_repo=self._repo)
