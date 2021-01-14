from PySide2.QtWidgets import QApplication

from slicereg.application.view_model import ViewModel
from slicereg.gui.window import MainWindow
from slicereg.gui.presenters import LoadAtlasPresenter, LoadSectionPresenter, MoveSectionPresenter, SelectChannelPresenter
from slicereg.application.load_atlas import BrainglobeAtlasRepo, LoadAtlasWorkflow
from slicereg.application.load_section import OmeTiffReader, LoadImageWorkflow
from slicereg.application.move_section import MoveSectionWorkflow
from slicereg.application.select_channel import SelectChannelWorkflow
from slicereg.application.shared.repos.section_repo import InMemorySectionRepo
from slicereg.application.provider import WorkflowProvider


def launch_gui():
    app = QApplication([])

    view_model = ViewModel()
    win = MainWindow(model=view_model)

    workflows = WorkflowProvider(
        load_section=LoadImageWorkflow(
            repo=InMemorySectionRepo(),
            presenter=LoadSectionPresenter(
                view=win
            ),
            reader=OmeTiffReader()
        ),
        select_channel=SelectChannelWorkflow(
            repo=InMemorySectionRepo(),
            presenter=SelectChannelPresenter(
                view=win
            )
        ),
        load_atlas=LoadAtlasWorkflow(
            repo=BrainglobeAtlasRepo(),
            presenter=LoadAtlasPresenter(
                view_model=view_model
            )
        ),
        move_section=MoveSectionWorkflow(
            repo=InMemorySectionRepo(),
            presenter=MoveSectionPresenter(
                view=win
            )
        )
    )
    win.register_workflows(app=workflows)
    app.exec_()


if __name__ == '__main__':
    launch_gui()
