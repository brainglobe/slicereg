from PySide2.QtWidgets import QApplication

from slicereg.commands.load_atlas import LoadAtlasCommand
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.gui.slice_view import SliceView
from slicereg.gui.view_model import ViewModel, LoadAtlasPresenter, LoadSectionPresenter, MoveSectionPresenter, \
    SelectChannelPresenter
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.window import MainWindow
from slicereg.io.ome_tiff import OmeTiffReader
from slicereg.repos.brainglobe_atlas import BrainglobeAtlasRepo
from slicereg.repos.inmemory_section import InMemorySectionRepo


def launch_gui():
    # Initialize the State
    view_model = ViewModel()
    repo = InMemorySectionRepo()

    # Wire up the Commands
    move_section = MoveSectionCommand(repo=repo, presenter=MoveSectionPresenter(view_model=view_model))
    select_channel = SelectChannelCommand(repo=repo, presenter=SelectChannelPresenter(view_model=view_model))
    load_atlas = LoadAtlasCommand(repo=BrainglobeAtlasRepo(), presenter=LoadAtlasPresenter(view_model=view_model))
    load_section = LoadImageCommand(repo=repo, presenter=LoadSectionPresenter(view_model=view_model), reader=OmeTiffReader())

    # Wire up the GUI
    app = QApplication([])

    volume_view = VolumeView()
    view_model.atlas_updated.connect(volume_view.on_atlas_update)
    view_model.section_loaded.connect(volume_view.on_section_loaded)
    view_model.section_moved.connect(volume_view.on_section_moved)
    view_model.channel_changed.connect(volume_view.on_channel_select)
    volume_view.move_section = move_section
    volume_view.select_channel = select_channel

    slice_view = SliceView()
    view_model.section_loaded.connect(slice_view.on_section_loaded)
    view_model.channel_changed.connect(slice_view.on_channel_select)
    slice_view.move_section = move_section

    window = MainWindow(
        title=view_model.main_title,
        volume_widget=volume_view.qt_widget,
        slice_widget=slice_view.qt_widget,
    )
    window.load_atlas = load_atlas
    window.load_section = load_section
    view_model.error_raised.connect(window.on_error_raised)

    # Start off with the first command
    load_atlas(resolution=25)

    # Start the Event Loop!
    app.exec_()


if __name__ == '__main__':
    launch_gui()
