import numpy as np
from PySide2.QtWidgets import QApplication

from slicereg import config
from slicereg.gui.commands import CommandProvider
from slicereg.gui.sidebar_view import SidebarView
from slicereg.gui.slice_view import SliceView
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.window import MainWindow
from slicereg.io.ome_tiff import OmeTiffReader
from slicereg.repos.atlas_repo import BrainglobeAtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo

np.set_printoptions(suppress=True, precision=2)


def launch_gui(create_qapp: bool = True, load_atlas_on_launch: bool = True):
    # Initialize the State
    commands = CommandProvider.from_repos(
        atlas_repo=BrainglobeAtlasRepo(),
        section_repo=InMemorySectionRepo(),
        tiff_reader=OmeTiffReader(),
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
