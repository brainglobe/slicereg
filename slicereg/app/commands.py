from __future__ import annotations

from dataclasses import dataclass, field

from slicereg.app.commands.get_coords import MapImageCoordToAtlasCoordCommand
from slicereg.app.commands.list_bgatlases import ListBgAtlasesCommand
from slicereg.app.commands.load_atlas import LoadBrainglobeAtlasCommand, LoadAtlasFromFileCommand
from slicereg.app.commands.load_section import LoadImageCommand
from slicereg.app.commands.move_section import MoveSectionCommand, UpdateSectionTransformCommand
from slicereg.app.commands.resample_section import ResampleSectionCommand
from slicereg.app.commands.select_channel import SelectChannelCommand
from slicereg.io.bg_atlasapi import BrainglobeAtlasReader
from slicereg.io.imio import ImioAtlasReader
from slicereg.io.tifffile import OmeTiffImageReader, TiffImageReader
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import SectionRepo


@dataclass(frozen=True)
class CommandProvider:
    _atlas_repo: AtlasRepo = field(default_factory=AtlasRepo)
    _section_repo: SectionRepo = field(default_factory=SectionRepo)
    _bgatlas_reader: BrainglobeAtlasReader = field(default_factory=BrainglobeAtlasReader)
    _atlas_file_reader: ImioAtlasReader = field(default_factory=ImioAtlasReader)
    _section_tiff_reader: TiffImageReader = field(default_factory=TiffImageReader)
    _section_ome_reader: OmeTiffImageReader = field(default_factory=OmeTiffImageReader)

    @property
    def load_atlas(self) -> LoadBrainglobeAtlasCommand:
        return LoadBrainglobeAtlasCommand(_repo=self._atlas_repo, _reader=self._bgatlas_reader)

    @property
    def load_section(self) -> LoadImageCommand:
        return LoadImageCommand(
            _repo=self._section_repo,
            _atlas_repo=self._atlas_repo,
            _ome_reader=self._section_ome_reader,
            _tiff_reader=self._section_tiff_reader
        )

    @property
    def load_atlas_from_file(self) -> LoadAtlasFromFileCommand:
        return LoadAtlasFromFileCommand(_repo=self._atlas_repo, _reader=self._atlas_file_reader)

    @property
    def list_bgatlases(self) -> ListBgAtlasesCommand:
        return ListBgAtlasesCommand(_reader=self._bgatlas_reader)

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
    def get_atlas_coord(self) -> MapImageCoordToAtlasCoordCommand:
        return MapImageCoordToAtlasCoordCommand(_repo=self._section_repo, _atlas_repo=self._atlas_repo)

    @property
    def resample_section(self) -> ResampleSectionCommand:
        return ResampleSectionCommand(_repo=self._section_repo, _atlas_repo=self._atlas_repo)
