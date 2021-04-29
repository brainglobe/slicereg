import os
import platform

import numpy as np
from PySide2.QtWidgets import QApplication
from packaging import version

from slicereg.gui.commands import CommandProvider
from slicereg.gui.model import AppModel
from slicereg.gui.views.sidebar import SidebarView, SidebarViewModel
from slicereg.gui.views.slice import SliceView, SliceViewModel
from slicereg.gui.views.volume import VolumeView, VolumeViewModel
from slicereg.gui.views.window import MainWindow, MainWindowViewModel
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo

np.set_printoptions(suppress=True, precision=2)


def is_mac_big_sur() -> bool:
    """
    platform.system(): 'Darwin'
    platform.release(): '20.3.0' or '20.4.0'
    platform.mac_ver(): ('10.16', ('', '', ''), 'arm64') or ('10.16', ('', '', ''), 'x86_64') or ('11.3', ('', '', ''), 'arm64')
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

    model = AppModel(_commands=commands)
    commands.load_atlas.atlas_updated.connect(model.on_atlas_update)
    commands.load_atlas_from_file.atlas_updated.connect(model.on_atlas_update)
    commands.load_section.section_loaded.connect(model.on_section_loaded)
    commands.select_channel.channel_changed.connect(model.on_channel_select)
    commands.resample_section.section_resampled.connect(model.on_section_resampled)
    commands.move_section.section_moved.connect(model.on_section_moved)
    commands.update_section.section_moved.connect(model.on_section_moved)
    commands.get_coord.coord_data_requested.connect(model.on_image_coordinate_highlighted)
    commands.list_bgatlases.atlas_list_updated.connect(model.on_bgatlas_list_update)

    slice_viewmodel = SliceViewModel(_model=model)
    slice_view = SliceView()
    slice_view.register(slice_viewmodel)

    volume_viewmodel = VolumeViewModel(_model=model)
    volume_view = VolumeView()
    volume_view.register(volume_viewmodel)

    sidebar_viewmodel = SidebarViewModel(_model=model)
    sidebar_view = SidebarView()
    sidebar_view.register(sidebar_viewmodel)

    window_viewmodel = MainWindowViewModel(_model=model)
    window = MainWindow(
        volume_widget=volume_view.qt_widget,
        slice_widget=slice_view.qt_widget,
        side_controls=sidebar_view.qt_widget,
    )
    window.register(window_viewmodel)


    # Start the Event Loop!
    if create_qapp:
        app.exec_()

    return window


if __name__ == '__main__':
    launch_gui()
