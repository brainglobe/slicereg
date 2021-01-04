import sys
from cx_Freeze import setup, Executable

setup(
    name="Multi-Slice Registration App",
    version="0.1",
    description="A slice registration app.",
    executables=[
        Executable(
            "main.py",
            base=None # "Win32GUI" if sys.platform == "win32" else None  # WIN32GUI makes it so the app launches without a terminal.
        ),
    ],
    options={
        "build_exe": {
            # "excludes": ["tkinter", "turtle"],
            "packages": ["vispy.app.backends._pyside2"],
            "includes": ["OpenGL.platform.win32"],
        }
    },
)
