from __future__ import annotations

from dataclasses import dataclass

from slicereg.commands.get_coords import GetPixelRegistrationDataCommand
from slicereg.commands.list_bgatlases import ListBgAtlasesCommand
from slicereg.commands.load_atlas import LoadBrainglobeAtlasCommand, LoadAtlasFromFileCommand
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand, UpdateSectionTransformCommand
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.io.imio import ImioAtlasReader
from slicereg.io.tifffile import OmeTiffImageReader, TiffImageReader
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo


@dataclass(frozen=True)
class CommandProvider:
    _atlas_repo: AtlasRepo
    _section_repo: InMemorySectionRepo

    @property
    def load_atlas(self) -> LoadBrainglobeAtlasCommand:
        return LoadBrainglobeAtlasCommand(_repo=self._atlas_repo, _reader=BrainglobeAtlasReader())

    @property
    def load_section(self) -> LoadImageCommand:
        return LoadImageCommand(
            _repo=self._section_repo,
            _atlas_repo=self._atlas_repo,
            _ome_reader=OmeTiffImageReader(),
            _tiff_reader=TiffImageReader()
        )

    @property
    def load_atlas_from_file(self) -> LoadAtlasFromFileCommand:
        return LoadAtlasFromFileCommand(_repo=self._atlas_repo, _reader=ImioAtlasReader())

    @property
    def list_bgatlases(self) -> ListBgAtlasesCommand:
        return ListBgAtlasesCommand(_reader=BrainglobeAtlasReader())

    @property
    def select_channel(self) -> SelectChannelCommand:
        return SelectChannelCommand(_repo=self._section_repo)

    @property
    def move_section(self) -> MoveSectionCommand:
        return MoveSectionCommand(_section_repo=self._section_repo, _atlas_repo=self._atlas_repo)

    @property
    def update_section(self) -> UpdateSectionTransformCommand:
        return UpdateSectionTransformCommand(_section_repo=self._section_repo, _atlas_repo=self._atlas_repo)

    @property
    def get_coord(self) -> GetPixelRegistrationDataCommand:
        return GetPixelRegistrationDataCommand(_repo=self._section_repo, _atlas_repo=self._atlas_repo)

    @property
    def resample_section(self) -> ResampleSectionCommand:
        return ResampleSectionCommand(_repo=self._section_repo, _atlas_repo=self._atlas_repo)
