from dataclasses import dataclass

from PySide2.QtWidgets import QApplication

from slicereg.commands.get_coords import GetPixelRegistrationDataCommand
from slicereg.commands.list_bgatlases import ListBgAtlasesCommand
from slicereg.commands.load_atlas import LoadAtlasCommand
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.commands.update_section_transform import UpdateSectionTransformCommand
from slicereg import config
from slicereg.gui.slice_view import SliceView
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.sidebar_view import SidebarView
from slicereg.gui.window import MainWindow
from slicereg.io.ome_tiff import OmeTiffReader
from slicereg.repos.atlas_repo import BrainglobeAtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo

import numpy as np

np.set_printoptions(suppress=True, precision=2)


@dataclass(frozen=True)
class CommandProvider:
    load_atlas: LoadAtlasCommand
    list_bgatlases: ListBgAtlasesCommand
    load_section: LoadImageCommand
    select_channel: SelectChannelCommand
    move_section: MoveSectionCommand
    update_section: UpdateSectionTransformCommand
    get_coord: GetPixelRegistrationDataCommand
    resample_section: ResampleSectionCommand


def launch_gui(create_qapp: bool = True, load_atlas_on_launch: bool = True):
    # Initialize the State
    section_repo = InMemorySectionRepo()
    atlas_repo = BrainglobeAtlasRepo()
    commands = CommandProvider(
        load_atlas=LoadAtlasCommand(_repo=atlas_repo),
        list_bgatlases=ListBgAtlasesCommand(_repo=atlas_repo),
        load_section=LoadImageCommand(_repo=section_repo, _atlas_repo=atlas_repo, _reader=OmeTiffReader()),
        select_channel=SelectChannelCommand(_repo=section_repo),
        move_section=MoveSectionCommand(_section_repo=section_repo, _atlas_repo=atlas_repo),
        update_section=UpdateSectionTransformCommand(_section_repo=section_repo, _atlas_repo=atlas_repo),
        get_coord=GetPixelRegistrationDataCommand(_repo=section_repo),
        resample_section=ResampleSectionCommand(_repo=section_repo, _atlas_repo=atlas_repo),
    )

    # Wire up the GUI
    if create_qapp:
        app = QApplication([])

    volume_view = VolumeView()
    slice_view = SliceView()
    sidebar_view = SidebarView()
    window = MainWindow(
        title=config.WINDOW_TITLE,
        volume_widget=volume_view.qt_widget,
        slice_widget=slice_view.qt_widget,
        side_controls=sidebar_view.qt_widget,
    )

    sidebar_view.load_atlas = commands.load_atlas  # type: ignore
    commands.load_atlas.atlas_updated.connect(volume_view.on_atlas_update)

    sidebar_view.list_brainglobe_atlases = commands.list_bgatlases  # type: ignore
    commands.list_bgatlases.atlas_list_updated.connect(sidebar_view.show_brainglobe_atlases)

    sidebar_view.load_section = commands.load_section  # type: ignore
    commands.load_section.section_loaded.connect(slice_view.on_section_loaded)
    commands.load_section.section_loaded.connect(volume_view.on_section_loaded)
    commands.load_section.section_loaded.connect(sidebar_view.on_section_loaded)

    volume_view.select_channel = commands.select_channel  # type: ignore
    commands.select_channel.channel_changed.connect(volume_view.on_channel_select)
    commands.select_channel.channel_changed.connect(slice_view.on_channel_select)

    volume_view.move_section = commands.move_section  # type: ignore
    slice_view.move_section = commands.move_section  # type: ignore
    sidebar_view.transform_section = commands.update_section  # type: ignore

    commands.move_section.section_moved.connect(volume_view.on_section_moved)
    commands.move_section.section_moved.connect(slice_view.on_section_moved)
    commands.update_section.section_moved.connect(volume_view.on_section_moved)
    commands.update_section.section_moved.connect(slice_view.on_section_moved)

    slice_view.get_coord_data = commands.get_coord  # type: ignore
    commands.get_coord.coord_data_requested.connect(window.on_image_coordinate_highlighted)

    sidebar_view.resample_section = commands.resample_section  # type: ignore
    commands.resample_section.section_resampled.connect(slice_view.on_section_resampled)
    commands.resample_section.section_resampled.connect(volume_view.on_section_resampled)

    # Start the Event Loop!
    if create_qapp:
        app.exec_()

    return window


if __name__ == '__main__':
    launch_gui()
