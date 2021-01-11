from slicereg.gui.window import MainWindow


def test_gui_launches_without_errors(qtbot):
    app = MainWindow()
    qtbot.addWidget(app.win)
