import sys

from PyQt6.QtWidgets import QApplication
from app import LoginWindow

import config


def main():
    base_url = config.BaseUrl()
    base_url.set_base_url()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
