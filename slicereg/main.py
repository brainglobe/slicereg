from PySide2.QtWidgets import QApplication

from slicereg.commands.load_atlas import LoadAtlasCommand
from slicereg.commands.provider import CommandProvider
from slicereg.gui.slice_view import SliceView
from slicereg.gui.view_model import ViewModel, LoadAtlasPresenter, LoadSectionPresenter, MoveSectionPresenter, \
    SelectChannelPresenter
from slicereg.gui.volume_view import VolumeView
from slicereg.gui.window import MainWindow
from slicereg.io.ome_tiff import OmeTiffReader
from slicereg.commands.load_section import LoadImageCommand
from slicereg.commands.move_section import MoveSectionCommand
from slicereg.commands.select_channel import SelectChannelCommand
from slicereg.repos.brainglobe_atlas import BrainglobeAtlasRepo
from slicereg.repos.inmemory_section import InMemorySectionRepo


def launch_gui():

    view_model = ViewModel()
    repo = InMemorySectionRepo()

    commands = CommandProvider(
        load_section=LoadImageCommand(
            repo=repo,
            presenter=LoadSectionPresenter(
                view_model=view_model
            ),
            reader=OmeTiffReader()
        ),
        select_channel=SelectChannelCommand(
            repo=repo,
            presenter=SelectChannelPresenter(
                view_model=view_model
            )
        ),
        load_atlas=LoadAtlasCommand(
            repo=BrainglobeAtlasRepo(),
            presenter=LoadAtlasPresenter(
                view_model=view_model
            )
        ),
        move_section=MoveSectionCommand(
            repo=repo,
            presenter=MoveSectionPresenter(
                view_model=view_model
            )
        )
    )

    app = QApplication([])

    volume_view = VolumeView(commands=commands)
    view_model.atlas_updated.connect(volume_view.on_atlas_update)
    view_model.section_loaded.connect(volume_view.on_section_loaded)
    view_model.section_moved.connect(volume_view.on_section_moved)
    view_model.channel_changed.connect(volume_view.on_channel_select)

    slice_view = SliceView(commands=commands)
    view_model.section_loaded.connect(slice_view.on_section_loaded)
    view_model.channel_changed.connect(slice_view.on_channel_select)

    window = MainWindow(
        title=view_model.main_title,
        commands=commands,
        volume_widget=volume_view.qt_widget,
        slice_widget=slice_view.qt_widget,
    )
    view_model.error_raised.connect(window.on_error_raised)
    app.exec_()


if __name__ == '__main__':
    launch_gui()
