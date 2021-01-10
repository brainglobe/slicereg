from src.gui.controller import Controller
from src.gui.presenter import LoadSectionPresenter
from src.gui.window import Window
from src.workflows.load_atlas.gui_view import GuiView
from src.workflows.load_atlas.load_atlas import LoadAtlasWorkflow
from src.workflows.load_atlas.presenter import GuiPresenter
from src.workflows.load_atlas.repo import BrainglobeAtlasRepo
from src.workflows.load_section.io import OmeTiffSerializer
from src.workflows.load_section.load_section import LoadSectionWorkflow
from src.workflows.load_section.repo import SectionRepo
from src.workflows.move_section.move_section import MoveSectionWorkflow
from src.workflows.select_channel import SelectChannelWorkflow

win = Window(title="Registration App")


repo = SectionRepo(
    serializer=OmeTiffSerializer()
)

from src.workflows.move_section.presenter import GuiPresenter as MSPresenter
from src.workflows.move_section.gui_view import GuiView as MSView


use_cases = Controller(
    view=win,
    load_section=LoadSectionWorkflow(
        repo=repo,
        presenter=LoadSectionPresenter(win=win),
    ),
    _select_channel=SelectChannelWorkflow(
        repo=repo,
    ),
    load_atlas=LoadAtlasWorkflow(
        repo=BrainglobeAtlasRepo(),
        presenter=GuiPresenter(
            view=GuiView(win=win)
        )
    ),
    move_section=MoveSectionWorkflow(
        repo=repo,
        presenter=MSPresenter(
            view=MSView(win=win)
        )
    )
)
win.register_use_cases(app=use_cases)
win.run()
