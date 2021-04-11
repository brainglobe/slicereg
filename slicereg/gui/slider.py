from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSlider, QLabel, QHBoxLayout


class LabelledSliderWidget:

    def __init__(self, min: int, max: int, label: str):
        self.layout = QHBoxLayout()

        self.slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.slider)

        self.value_label = QLabel(text='0')
        self.layout.addWidget(self.value_label)

        self.name_label = QLabel(text=label)
        self.layout.addWidget(self.name_label)

        self.slider.setMinimum(int(min))
        self.slider.setMaximum(int(max))
        self.slider.valueChanged.connect(self._on_slider_valuechange)

    def _on_slider_valuechange(self, value: int):
        self.value_label.setText(str(value))

    def set_value(self, value: int):
        self.slider.setValue(value)

    @property
    def connect(self):
        return self.slider.valueChanged.connect
