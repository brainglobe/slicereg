from src.ui.provider import UseCaseProvider
from src.ui.window import Window, Presenter
from src.repositiories.atlas import BGAtlasAllenRepo
from src.repositiories.section import InMemorySectionRepo

win = Window(title="Registration App")

presenter = Presenter(win=win)
use_cases = UseCaseProvider(
    section_repo=InMemorySectionRepo(),
    atlas_repo=BGAtlasAllenRepo(),
    load_atlas_presenter=presenter,
    select_channel_presenter=presenter,
    load_section_presenter=presenter,
    move_section_presenter=presenter,
)
win.register_use_cases(app=use_cases)
win.run()
