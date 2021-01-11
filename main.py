from src.gui.main_view import MainView
from src.workflows.load_atlas.presenter import LoadAtlasPresenter
from src.workflows.load_atlas.repo import BrainglobeAtlasRepo
from src.workflows.load_atlas.workflow import LoadAtlasWorkflow
from src.workflows.load_section.presenter import LoadSectionPresenter
from src.workflows.load_section.reader import OmeTiffReader
from src.workflows.load_section.workflow import LoadSectionWorkflow
from src.workflows.move_section.presenter import MoveSectionPresenter
from src.workflows.move_section.workflow import MoveSectionWorkflow
from src.workflows.select_channel.presenter import SelectChannelPresenter
from src.workflows.select_channel.workflow import SelectChannelWorkflow
from src.workflows.shared.repos.section_repo import InMemorySectionRepo
from src.workflows.workflowprovider import WorkflowProvider

win = MainView(title="Registration App")

use_cases = WorkflowProvider(
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
win.register_workflows(app=use_cases)
win.run()
