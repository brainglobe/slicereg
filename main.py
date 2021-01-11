from src.gui.window import Window
from src.workflows.load_atlas.workflow import LoadAtlasWorkflow
from src.workflows.load_atlas.presenter import GuiPresenter
from src.workflows.load_atlas.repo import BrainglobeAtlasRepo
from src.workflows.load_section.workflow import LoadSectionWorkflow
from src.workflows.load_section.presenter import GuiPresenter as LSPresenter
from src.workflows.load_section.reader import OmeTiffReader
from src.workflows.move_section.workflow import MoveSectionWorkflow
from src.workflows.move_section.presenter import GuiPresenter as MSPresenter
from src.workflows.workflowprovider import WorkflowProvider
from src.workflows.select_channel.workflow import SelectChannelWorkflow
from src.workflows.select_channel.presenter import GuiView
from src.workflows.shared.repos.section_repo import InMemorySectionRepo

win = Window(title="Registration App")

use_cases = WorkflowProvider(
    load_section=LoadSectionWorkflow(
        repo=InMemorySectionRepo(),
        presenter=LSPresenter(
            win=win
        ),
        reader=OmeTiffReader()
    ),
    select_channel=SelectChannelWorkflow(
        repo=InMemorySectionRepo(),
        presenter=GuiView(
            win=win
        )
    ),
    load_atlas=LoadAtlasWorkflow(
        repo=BrainglobeAtlasRepo(),
        presenter=GuiPresenter(
            win=win
        )
    ),
    move_section=MoveSectionWorkflow(
        repo=InMemorySectionRepo(),
        presenter=MSPresenter(
            win=win
        )
    )
)
win.register_workflows(app=use_cases)
win.run()
