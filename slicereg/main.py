from PySide2.QtWidgets import QApplication

from slicereg.application.commands.provider import CommandProvider
from slicereg.gui.view_model import ViewModel
from slicereg.gui.window import MainWindow
from slicereg.gui.presenters import LoadAtlasPresenter, LoadSectionPresenter, MoveSectionPresenter, SelectChannelPresenter
from slicereg.application.commands.load_atlas import LoadAtlasCommand
from slicereg.application.io import OmeTiffReader
from slicereg.application.commands.load_section import LoadImageCommand
from slicereg.application.commands.move_section import MoveSectionCommand
from slicereg.application.commands.select_channel import SelectChannelCommand
from slicereg.repos.bgatlas_repo import BrainglobeAtlasRepo
from slicereg.repos.section_repo import InMemorySectionRepo


def launch_gui():
    app = QApplication([])

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

    win = MainWindow(model=view_model)
    win.register_commands(app=commands)
    app.exec_()


if __name__ == '__main__':
    launch_gui()
