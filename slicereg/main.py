from PySide2.QtWidgets import QApplication

from slicereg.commands.load_atlas import LoadAtlasCommand
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg import config
from slicereg.gui.slice_view import SliceView
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.window import MainWindow
from slicereg.io.ome_tiff import OmeTiffReader
from slicereg.repos.atlas_repo import BrainglobeAtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo



def launch_gui(create_qapp: bool = True, load_atlas_on_launch: bool = True):
    # Initialize the State
    repo = InMemorySectionRepo()

    # Wire up the GUI
    if create_qapp:
        app = QApplication([])

    volume_view = VolumeView()
    slice_view = SliceView()
    window = MainWindow(
        title=config.WINDOW_TITLE,
        volume_widget=volume_view.qt_widget,
        slice_widget=slice_view.qt_widget,
    )

    if config.FEATURE_BRAINGLOBE_ATLAS:
        load_atlas = LoadAtlasCommand(_repo=BrainglobeAtlasRepo())
        window.load_atlas = load_atlas  # type: ignore
        load_atlas.atlas_updated.connect(volume_view.on_atlas_update)

        # Start off with the first command
        if load_atlas_on_launch:
            load_atlas(resolution=25)

    if config.FEATURE_VIEW_SECTION:
        load_section = LoadImageCommand(_repo=repo, _reader=OmeTiffReader())
        window.load_section = load_section  # type: ignore
        load_section.section_loaded.connect(slice_view.on_section_loaded)
        load_section.section_loaded.connect(volume_view.on_section_loaded)

        select_channel = SelectChannelCommand(_repo=repo)
        volume_view.select_channel = select_channel  # type: ignore
        select_channel.channel_changed.connect(volume_view.on_channel_select)
        select_channel.channel_changed.connect(slice_view.on_channel_select)


    if config.FEATURE_VIEW_SECTION and config.FEATURE_MOVE_SECTION:
        move_section = MoveSectionCommand(_repo=repo)
        volume_view.move_section = move_section  # type: ignore
        slice_view.move_section = move_section  # type: ignore
        move_section.section_moved.connect(volume_view.on_section_moved)





    # Start the Event Loop!
    if create_qapp:
        app.exec_()

    return window


if __name__ == '__main__':
    launch_gui()
