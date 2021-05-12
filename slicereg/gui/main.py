import os
import platform

import numpy as np
from PySide2.QtWidgets import QApplication
from packaging import version

from slicereg.app.commands import CommandProvider
from slicereg.app.app_model import AppModel
from slicereg.gui.atlas_section_window import AtlasSectionViewModel, AtlasSectionView
from slicereg.gui.sidebar import SidebarViewModel, SidebarView
from slicereg.gui.slice_window import SliceViewModel, SliceView
from slicereg.gui.volume_window import VolumeViewModel, VolumeView
from slicereg.gui.main_window import MainWindowView, MainWindowViewModel
from slicereg.repos.atlas_repo import AtlasRepo
from slicereg.repos.section_repo import SectionRepo

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
    commands = CommandProvider(_atlas_repo=AtlasRepo(), _section_repo=SectionRepo())

    # Wire up the GUI
    if create_qapp:
        app = QApplication([])

    model = AppModel(_commands=commands)

    coronal_section_viewmodel = AtlasSectionViewModel(axis=0, _model=model)
    coronal_section_view = AtlasSectionView()
    coronal_section_view.register(coronal_section_viewmodel)

    axial_section_viewmodel = AtlasSectionViewModel(axis=1, _model=model)
    axial_section_view = AtlasSectionView()
    axial_section_view.register(axial_section_viewmodel)

    sagittal_section_viewmodel = AtlasSectionViewModel(axis=2, _model=model)
    sagittal_section_view = AtlasSectionView()
    sagittal_section_view.register(sagittal_section_viewmodel)

    slice_viewmodel = SliceViewModel(_model=model)
    slice_view = SliceView()
    slice_view.register(slice_viewmodel)

    volume_view = VolumeView(_model=VolumeViewModel(_model=model))

    sidebar_viewmodel = SidebarViewModel(_model=model)
    sidebar_view = SidebarView()
    sidebar_view.register(sidebar_viewmodel)

    window_viewmodel = MainWindowViewModel(_model=model)
    window = MainWindowView(
        coronal_widget=coronal_section_view.qt_widget,
        axial_widget=axial_section_view.qt_widget,
        sagittal_widget=sagittal_section_view.qt_widget,
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
