from typing import Callable

from PySide2.QtWidgets import QSlider, QLabel, QHBoxLayout
from PySide2.QtCore import Qt


class LabelledSliderWidget:

    def __init__(self, min: int, max: int, default_text: str):

        self.layout = QHBoxLayout()

        self.slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.slider)

        self.label = QLabel(text=default_text)
        self.layout.addWidget(self.label)

        self.slider.setMinimum(int(min))
        self.slider.setMaximum(int(max))
        self.slider.valueChanged.connect(self._on_slider_valuechange)
        self.slider.sliderReleased.connect(self._on_slider_release)
        
    def _on_slider_valuechange(self, value: int):
        self.label.setText(str(value))
        
    def _on_slider_release(self):
        self.label.setText(str(self.value))

    def connect(self, fun: Callable[[], None]):
        self.slider.sliderReleased.connect(fun)

    @property
    def value(self) -> float:
        return self.slider.value()