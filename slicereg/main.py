from PySide2.QtWidgets import QApplication

from slicereg.gui.window import MainWindow
from slicereg.gui.presenters import LoadAtlasPresenter, LoadSectionPresenter, MoveSectionPresenter, SelectChannelPresenter
from slicereg.workflows.load_atlas import BrainglobeAtlasRepo, LoadAtlasWorkflow
from slicereg.workflows.load_section import OmeTiffReader, LoadSectionWorkflow
from slicereg.workflows.move_section import MoveSectionWorkflow
from slicereg.workflows.select_channel import SelectChannelWorkflow
from slicereg.workflows.shared.repos.section_repo import InMemorySectionRepo
from slicereg.workflows.provider import WorkflowProvider


def launch_gui():
    app = QApplication([])
    win = MainWindow()

    workflows = WorkflowProvider(
        load_section=LoadSectionWorkflow(
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
                view=win
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
