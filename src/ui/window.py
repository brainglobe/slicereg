from typing import Optional

from PySide2.QtCore import QObject
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QPushButton, QFileDialog, QButtonGroup, \
    QHBoxLayout
from numpy import ndarray
from vispy.app import Timer

from src.ui.slice_view import SliceView
from src.ui.volume_view import VolumeView
from src.use_cases.load_atlas import BaseLoadAtlasPresenter
from src.use_cases.load_section import BaseLoadSectionPresenter
from src.use_cases.move_section import BaseMoveSectionPresenter
from src.ui.provider import UseCaseProvider
from src.use_cases.select_channel import BaseSelectChannelPresenter


def restart_timer(timer: Timer, iterations=1) -> None:
    """Restarts a Vispy Timer, even if it is already running."""
    timer.stop()
    timer.start(iterations=iterations)


class Window(QObject):

    def __init__(self, title):
        self.use_cases: Optional[UseCaseProvider] = None
        self._qt_app = QApplication([])
        self.win = QMainWindow()
        self._default_window_title = title

        widget = QWidget()
        self.win.setCentralWidget(widget)

        main_layout = QHBoxLayout()
        widget.setLayout(main_layout)

        self.slice_view = SliceView()
        main_layout.addWidget(self.slice_view.qt_widget)

        self.volume_view = VolumeView()
        main_layout.addWidget(self.volume_view.qt_widget)

        side_layout = QVBoxLayout()
        main_layout.addLayout(side_layout)

        load_image_button = QPushButton("Load Section")
        side_layout.addWidget(load_image_button)
        load_image_button.clicked.connect(self.show_load_image_dialog)

        # Atlas BUttons
        button_hbox = QHBoxLayout()
        side_layout.addLayout(button_hbox)

        atlas_buttons = QButtonGroup(self.win)
        atlas_buttons.setExclusive(True)
        atlas_buttons.buttonToggled.connect(self.atlas_button_toggled)

        for resolution in [100, 25, 10]:
            atlas_button = QPushButton(f"{resolution}um")
            atlas_button.setCheckable(True)
            button_hbox.addWidget(atlas_button)
            atlas_buttons.addButton(atlas_button)

            # The 10um atlas takes way too long to download at the moment.
            # It needs some kind of progress bar or async download feature to be useful.
            # The disabled button here shows it as an option for the future, but keeps it from being used.
            if resolution == 10:
                atlas_button.setDisabled(True)

        self.title_reset_timer = Timer(interval=2, connect=lambda e: self._show_default_window_title(), iterations=1,
                                       start=False)
        self._show_default_window_title()
        self.win.show()

    def atlas_button_toggled(self, button: QPushButton, is_checked: bool):
        if not is_checked:  # Don't do anything for the button being unselected.
            return

        resolution_label = button.text()
        resolution = int("".join(filter(str.isdigit, resolution_label)))
        self.use_cases.load_atlas(resolution=resolution)

    # Command Routing
    def show_load_image_dialog(self):
        if self.use_cases is None:
            return
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.win,
            caption="Load Image",
            dir="data/RA_10X_scans/MEA",
            filter="OME-TIFF (*.ome.tiff)"
        )
        if not filename:
            return
        self.use_cases.load_section(filename=filename)

    # Controller Code

    def register_use_cases(self, app: UseCaseProvider):
        self.use_cases = app
        self.volume_view.register_use_cases(app=app)
        self.slice_view.register_use_cases(app=app)
        self.use_cases.load_atlas(resolution=25)

    def run(self):
        self._qt_app.exec_()

    # View Code

    def _show_default_window_title(self):
        self.win.setWindowTitle(self._default_window_title)

    def show_temp_title(self, title: str) -> None:
        self.win.setWindowTitle(title)
        restart_timer(self.title_reset_timer)


class Presenter(BaseLoadAtlasPresenter, BaseSelectChannelPresenter, BaseLoadSectionPresenter, BaseMoveSectionPresenter):

    def __init__(self, win: Window):
        self.win = win

    def show_atlas(self, volume: ndarray, transform: ndarray):
        self.win.volume_view.view_atlas(volume=volume, transform=transform)

    def show_error(self, msg: str) -> None:
        self.win.show_temp_title(msg)

    def update_section_image(self, image: ndarray):
        self.win.volume_view.update_image(image=image)
        self.win.slice_view.update_slice_image(image=image)

    def update_section_transform(self, transform: ndarray):
        self.win.volume_view.update_transform(transform=transform)

    def show_section(self, image: ndarray, ref_image: ndarray, transform: Optional[ndarray] = None) -> None:
        self.win.volume_view.view_section(image=image, transform=transform)
        self.win.slice_view.show_new_slice(slice=image, ref_slice=ref_image)
