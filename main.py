from src.gui.window import Window
from src.workflows.load_atlas.load_atlas import LoadAtlasWorkflow
from src.workflows.load_atlas.presenter import GuiPresenter, GuiPresenter
from src.workflows.load_atlas.repo import BrainglobeAtlasRepo
from src.workflows.load_section.load_section import LoadSectionWorkflow
from src.workflows.load_section.reader import OmeTiffReader
from src.workflows.load_section.presenter import GuiPresenter as LSPresenter
from src.workflows.move_section.gui_view import GuiView as MSView
from src.workflows.move_section.move_section import MoveSectionWorkflow
from src.workflows.move_section.presenter import GuiPresenter as MSPresenter
from src.workflows.provider import Provider
from src.workflows.select_channel.gui_view import GuiView as SCView
from src.workflows.select_channel.presenter import GuiPresenter as SCPresenter
from src.workflows.select_channel.select_channel import SelectChannelWorkflow
from src.workflows.shared.repos.section_repo import InMemorySectionRepo

win = Window(title="Registration App")

use_cases = Provider(
    load_section=LoadSectionWorkflow(
        repo=InMemorySectionRepo(),
        presenter=LSPresenter(
            win=win
        ),
        reader=OmeTiffReader()
    ),
    select_channel=SelectChannelWorkflow(
        repo=InMemorySectionRepo(),
        presenter=SCPresenter(
            view=SCView(
                win=win
            )
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
            view=MSView(win=win)
        )
    )
)
win.register_use_cases(app=use_cases)
win.run()
