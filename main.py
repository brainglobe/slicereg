from src.use_cases.provider import UseCaseProvider
from src.gui_app.window import Window, Presenter
from src.repositiories.atlas import BGAtlasAllenRepo
from src.repositiories.section import InMemorySectionRepo

win = Window(title="Registration App")

use_cases = UseCaseProvider(
    section_repo=InMemorySectionRepo(),
    atlas_repo=BGAtlasAllenRepo(),
    load_atlas_presenter=Presenter(win=win),
    select_channel_presenter=Presenter(win=win),
    load_section_presenter=Presenter(win=win),
    move_section_presenter=Presenter(win=win),
)
win.register_use_cases(app=use_cases)
win.run()
