from __future__ import annotations

from dataclasses import dataclass, field

from slicereg.commands.get_coords import MapImageCoordToAtlasCoordCommand
from slicereg.commands.list_bgatlases import ListBgAtlasesCommand
from slicereg.commands.load_atlas import LoadBrainglobeAtlasCommand, LoadAtlasFromFileCommand
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand, UpdateSectionTransformCommand
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.io.brainglobe.atlas import BrainglobeAtlasReader
from slicereg.io.imio.atlas import ImioAtlasReader
from slicereg.io.tifffile.image import TiffImageReader, OmeTiffImageReader
from slicereg.commands.base import BaseRepo


@dataclass(frozen=True)
class CommandProvider:
    _repo: BaseRepo
    _bgatlas_reader: BrainglobeAtlasReader = field(default_factory=BrainglobeAtlasReader)
    _atlas_file_reader: ImioAtlasReader = field(default_factory=ImioAtlasReader)
    _section_tiff_reader: TiffImageReader = field(default_factory=TiffImageReader)
    _section_ome_reader: OmeTiffImageReader = field(default_factory=OmeTiffImageReader)

    @property
    def load_atlas(self) -> LoadBrainglobeAtlasCommand:
        return LoadBrainglobeAtlasCommand(_repo=self._repo, _reader=self._bgatlas_reader)

    @property
    def load_section(self) -> LoadImageCommand:
        return LoadImageCommand(
            _repo=self._repo,
            _ome_reader=self._section_ome_reader,
            _tiff_reader=self._section_tiff_reader
        )

    @property
    def load_atlas_from_file(self) -> LoadAtlasFromFileCommand:
        return LoadAtlasFromFileCommand(_repo=self._repo, _reader=self._atlas_file_reader)

    @property
    def list_bgatlases(self) -> ListBgAtlasesCommand:
        return ListBgAtlasesCommand(_reader=self._bgatlas_reader)

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
