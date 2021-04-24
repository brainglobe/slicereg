import numpy as np
from PySide2.QtWidgets import QApplication

from slicereg.gui import config
from slicereg.gui.commands import CommandProvider
from slicereg.gui.sidebar_view import SidebarView
from slicereg.gui.slice_view import SliceView
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.window import MainWindow
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo

np.set_printoptions(suppress=True, precision=2)


def launch_gui(create_qapp: bool = True):
    # Initialize the State
    commands = CommandProvider.from_repos(
        atlas_repo=AtlasRepo(),
        section_repo=InMemorySectionRepo(),
    )

    # Wire up the GUI
    if create_qapp:
        app = QApplication([])

    volume_view = VolumeView(commands=commands)
    slice_view = SliceView(commands=commands)
    sidebar_view = SidebarView(commands=commands)
    window = MainWindow(
        title=config.WINDOW_TITLE,
        volume_widget=volume_view.qt_widget,
        slice_widget=slice_view.qt_widget,
        side_controls=sidebar_view.qt_widget,
    )

    # Window View
    commands.get_coord.coord_data_requested.connect(window.on_image_coordinate_highlighted)

    # Sidebar View
    commands.list_bgatlases.atlas_list_updated.connect(sidebar_view.show_brainglobe_atlases)


    # Volume View
    commands.load_atlas.atlas_updated.connect(volume_view.on_atlas_update)
    commands.load_atlas_from_file.atlas_updated.connect(volume_view.on_atlas_update)
    commands.load_section.section_loaded.connect(volume_view.on_section_loaded)
    commands.select_channel.channel_changed.connect(volume_view.on_channel_select)
    commands.move_section.section_moved.connect(volume_view.on_section_moved)
    commands.update_section.section_moved.connect(volume_view.on_section_moved)
    commands.resample_section.section_resampled.connect(volume_view.on_section_resampled)

    # Slice View
    commands.load_section.section_loaded.connect(slice_view.on_section_loaded)
    commands.select_channel.channel_changed.connect(slice_view.on_channel_select)
    commands.move_section.section_moved.connect(slice_view.on_section_moved)
    commands.update_section.section_moved.connect(slice_view.on_section_moved)
    commands.resample_section.section_resampled.connect(slice_view.on_section_resampled)

    # Start the Event Loop!
    if create_qapp:
        app.exec_()

    return window


if __name__ == '__main__':
    launch_gui()
