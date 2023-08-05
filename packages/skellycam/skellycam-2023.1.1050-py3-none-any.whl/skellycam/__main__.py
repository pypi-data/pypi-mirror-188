# __main__.py
import sys
from pathlib import Path


try:
    from skellycam.qt_gui.qt_gui_main import qt_gui_main
except Exception as e:
    base_package_path = Path(__file__).parent.parent
    print(f"adding base_package_path: {base_package_path} : to sys.path")
    sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path
    from skellycam.qt_gui.qt_gui_main import qt_gui_main


def main():
    qt_gui_main()


if __name__ == "__main__":
    print(f"Running `skellycam.__main__` from - {__file__}")

    main()
