from slicereg.gui.main_view import MainWindow


def test_gui_launches_without_errors(qtbot):
    app = MainWindow()
    qtbot.addWidget(app.win)
