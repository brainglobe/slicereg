from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSlider, QLabel, QHBoxLayout


class LabelledSliderWidget:

    def __init__(self, min: int, max: int, label: str):
        self.layout = QHBoxLayout()

        self.slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.slider)

        self.label = QLabel(text=label)
        self.layout.addWidget(self.label)

        self.slider.setMinimum(int(min))
        self.slider.setMaximum(int(max))
        self.slider.valueChanged.connect(self._on_slider_valuechange)

    def _on_slider_valuechange(self, value: int):
        self.label.setText(str(value))

    @property
    def connect(self):
        return self.slider.valueChanged.connect
