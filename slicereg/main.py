from PySide2.QtWidgets import QApplication

from slicereg.commands.load_atlas import LoadAtlasCommand
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.gui.slice_view import SliceView
from slicereg.gui.view_model import LoadAtlasPresenter, LoadSectionPresenter, MoveSectionPresenter, \
    SelectChannelPresenter
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.window import MainWindow
from slicereg.io.ome_tiff import OmeTiffReader
from slicereg.repos.atlas_repo import BrainglobeAtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo


def launch_gui(create_qapp: bool = True, load_atlas_on_launch: bool = True):
    # Initialize the State
    repo = InMemorySectionRepo()

    # Wire up the Commands
    move_section_presenter = MoveSectionPresenter()
    move_section = MoveSectionCommand(repo=repo, presenter=move_section_presenter)
    select_channel_presenter = SelectChannelPresenter()
    select_channel = SelectChannelCommand(repo=repo, presenter=select_channel_presenter)
    load_atlas_presenter = LoadAtlasPresenter()
    load_atlas = LoadAtlasCommand(repo=BrainglobeAtlasRepo(), presenter=load_atlas_presenter)

    load_section_presenter = LoadSectionPresenter()
    load_section = LoadImageCommand(repo=repo, presenter=load_section_presenter, reader=OmeTiffReader())

    # Wire up the GUI
    if create_qapp:
        app = QApplication([])

    volume_view = VolumeView()
    load_atlas_presenter.atlas_updated.connect(volume_view.on_atlas_update)
    load_section_presenter.section_loaded.connect(volume_view.on_section_loaded)
    move_section_presenter.section_moved.connect(volume_view.on_section_moved)
    select_channel_presenter.channel_changed.connect(volume_view.on_channel_select)
    volume_view.move_section = move_section  # type: ignore
    volume_view.select_channel = select_channel  # type: ignore

    slice_view = SliceView()
    load_section_presenter.section_loaded.connect(slice_view.on_section_loaded)
    select_channel_presenter.channel_changed.connect(slice_view.on_channel_select)
    slice_view.move_section = move_section  # type: ignore

    window = MainWindow(
        title="Default Title",
        volume_widget=volume_view.qt_widget,
        slice_widget=slice_view.qt_widget,
    )
    window.load_atlas = load_atlas  # type: ignore
    window.load_section = load_section  # type: ignore

    # Start off with the first command
    if load_atlas_on_launch:
        load_atlas(resolution=25)

    # Start the Event Loop!
    if create_qapp:
        app.exec_()

    return window


if __name__ == '__main__':
    launch_gui()
