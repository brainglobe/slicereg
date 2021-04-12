from __future__ import annotations

from dataclasses import dataclass

from slicereg.commands.get_coords import GetPixelRegistrationDataCommand
from slicereg.commands.list_bgatlases import ListBgAtlasesCommand
from slicereg.commands.load_atlas import LoadAtlasCommand
from slicereg.commands.load_atlas_from_file import LoadAtlasFromFileCommand
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.commands.update_section_transform import UpdateSectionTransformCommand
from slicereg.io.ome_tiff import OmeTiffReader
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo


@dataclass(frozen=True)
class CommandProvider:
    load_atlas: LoadAtlasCommand
    load_atlas_from_file: LoadAtlasFromFileCommand
    list_bgatlases: ListBgAtlasesCommand
    load_section: LoadImageCommand
    select_channel: SelectChannelCommand
    move_section: MoveSectionCommand
    update_section: UpdateSectionTransformCommand
    get_coord: GetPixelRegistrationDataCommand
    resample_section: ResampleSectionCommand

    @classmethod
    def from_repos(cls, atlas_repo: AtlasRepo, section_repo: InMemorySectionRepo, tiff_reader: OmeTiffReader) -> CommandProvider:
        return cls(
            load_atlas=LoadAtlasCommand(_repo=atlas_repo),
            load_atlas_from_file=LoadAtlasFromFileCommand(_repo=atlas_repo),
            list_bgatlases=ListBgAtlasesCommand(_repo=atlas_repo),
            load_section=LoadImageCommand(_repo=section_repo, _atlas_repo=atlas_repo, _reader=tiff_reader),
            select_channel=SelectChannelCommand(_repo=section_repo),
            move_section=MoveSectionCommand(_section_repo=section_repo, _atlas_repo=atlas_repo),
            update_section=UpdateSectionTransformCommand(_section_repo=section_repo, _atlas_repo=atlas_repo),
            get_coord=GetPixelRegistrationDataCommand(_repo=section_repo),
            resample_section=ResampleSectionCommand(_repo=section_repo, _atlas_repo=atlas_repo),
        )
