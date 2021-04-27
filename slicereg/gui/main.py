import os
import platform

import numpy as np
from PySide2.QtWidgets import QApplication
from packaging import version

from slicereg.gui import config
from slicereg.gui.commands import CommandProvider
from slicereg.gui.model import AppModel
from slicereg.gui.sidebar_view import SidebarView, SidebarViewModel
from slicereg.gui.slice_view import SliceView, SliceViewModel
from slicereg.gui.volume_view import VolumeView, VolumeViewModel
from slicereg.gui.window import MainWindow
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo

np.set_printoptions(suppress=True, precision=2)


def is_mac_big_sur() -> bool:
    """
    platform.system(): 'Darwin'
    platform.release(): '20.3.0'
    platform.mac_ver(): ('10.16', ('', '', ''), 'arm64') or ('10.16', ('', '', ''), 'x86_64')
    """
    return platform.system() == 'Darwin' and version.parse(platform.mac_ver()[0]) >= version.parse('10.16')


def launch_gui(create_qapp: bool = True):

    # Set special os environ if mac Big Sur is being used
    # https://stackoverflow.com/questions/64818879/is-there-any-solution-regarding-to-pyqt-library-doesnt-work-in-mac-os-big-sur
    if is_mac_big_sur():
        os.environ['QT_MAC_WANTS_LAYER'] = '1'

    # Initialize the State
    commands = CommandProvider.from_repos(
        atlas_repo=AtlasRepo(),
        section_repo=InMemorySectionRepo(),
    )



    # Wire up the GUI
    if create_qapp:
        app = QApplication([])

    model = AppModel()
    volume_view = VolumeView(commands=commands, model=VolumeViewModel(_model=model))
    slice_view = SliceView(commands=commands, model=SliceViewModel(_model=model))
    sidebar_view = SidebarView(
        commands=commands, model=SidebarViewModel(_model=model))
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
