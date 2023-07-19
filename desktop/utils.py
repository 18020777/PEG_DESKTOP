from PyQt6.QtWidgets import QApplication


class WindowUtils:
    @staticmethod
    def center_window(window):
        screen_geometry = QApplication.instance().primaryScreen().availableGeometry()
        window_width = window.width()
        window_height = window.height()
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        window.setGeometry(x, y, window_width, window_height)
