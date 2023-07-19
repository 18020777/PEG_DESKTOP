from datetime import datetime, timedelta

from PyQt6.QtCore import Qt, QSize, QTimer, QDate
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame, QLabel, QListWidgetItem

import auth
import config as cf
import utils as u
from bookings import APIBookingsClient, BookingElement
from pui.loginwindow import Ui_LoginWindow
from pui.mainwindow import Ui_MainWindow


class LoginWindow(Ui_LoginWindow, QMainWindow):

    def __init__(self):
        super().__init__()
        self.mainApp = None
        self.setupUi(self)
        self.setup_links()
        u.WindowUtils.center_window(self)

    def login(self):
        username = self.editUsername.text()
        password = self.editPassword.text()
        token_getter = auth.TokenGetter()
        token_auth = auth.TokenAuth(token_getter.get_token(username, password))
        if token_auth.authorization():
            self.mainApp = MainWindow(token_auth)
            self.mainApp.show()
            self.close()

    def setup_links(self):
        self.buttonLogin.clicked.connect(self.login)

    def keyPressEvent(self, event: QKeyEvent):
        # Handle key press events
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            # Simulate button click when "Enter" key is pressed
            self.buttonLogin.click()
        else:
            # Propagate other key press events to the base class
            super().keyPressEvent(event)


class MainWindow(Ui_MainWindow, QWidget):
    def __init__(self, token_auth):
        super().__init__()
        self.token_auth = token_auth
        self.timer = QTimer()
        self.setupUi(self)
        u.WindowUtils.center_window(self)
        self.set_date()
        self.set_legend()
        self.fetch_bookings()
        self.setup_links()
        self.timer.start(15000)  # 15 secondes (15 000 millisecondes)

    def setup_links(self):
        self.dateToday.dateChanged.connect(self.fetch_bookings)
        self.timer.timeout.connect(self.fetch_bookings)

    def set_date(self):
        self.dateToday.setDate(QDate.currentDate())

    def set_legend(self):
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.labelTocome.setStyleSheet("QLabel#labelTocome { color: " + cf.tocome + "; }")
        self.labelStarted.setStyleSheet("QLabel#labelStarted { color: " + cf.started + "; }")
        self.labelSoon.setStyleSheet("QLabel#labelSoon { color: " + cf.soon + "; }")
        self.labelFinished.setStyleSheet("QLabel#labelFinished { color: " + cf.finished + "; }")

    def fetch_bookings(self):
        self.bookingList.clear()
        bookings = APIBookingsClient(self.token_auth.get_token(), str(self.dateToday.date().toPyDate())).get_data()
        if bookings is not None:
            for booking in bookings['results']:
                game = BookingElement(booking, self.token_auth.get_token())
                frame = QFrame(objectName="bookingItemFrame")  # Ajout du QFrame avec le nom d'objet
                frame.setStyleSheet(
                    "QFrame#bookingItemFrame { background-color: #1e1e1e; border-radius: 5px; }")
                frame_layout = QVBoxLayout(frame)
                frame_layout.setContentsMargins(10, 10, 10, 10)

                label = QLabel("")
                label_str = (f"ID: {game.id}   |   User: {game.username} ({game.first_name} "
                             f"{game.last_name} - {game.email})   "
                             f"|   Time: {game.time}   |   Players: {game.num_players}")
                label.setObjectName("bookingItemLabel")
                if game.start_time is not None:
                    label_str = label_str + f"   |   Start time: {game.start_time}"
                    if game.chrono is not None and str(game.chrono) != "00:00:00":
                        label_str = label_str + f"   |   Chrono: {game.chrono}"
                        label.setStyleSheet(
                            "QLabel#bookingItemLabel { color: " + cf.finished + "; font-size: " + cf.fsize + "; }")
                    elif game.start_dt + game.duration < datetime.now() - timedelta(minutes=5):
                        label.setStyleSheet(
                            "QLabel#bookingItemLabel { color: " + cf.soon + "; font-size: " + cf.fsize + "; }")
                    else:
                        label.setStyleSheet(
                            "QLabel#bookingItemLabel { color: " + cf.started + "; font-size: " + cf.fsize + "; }")
                else:
                    label.setStyleSheet(
                        "QLabel#bookingItemLabel { color: " + cf.tocome + "; font-size: " + cf.fsize + "; }")
                label.setText(label_str)

                frame_layout.addWidget(label)

                item = QListWidgetItem()  # Ajouter un nouvel élément à la liste
                item.setSizeHint(QSize(0, 50))  # Définir la taille de l'élément en fonction du QFrame
                self.bookingList.addItem(item)  # Add item to the bookingList widget
                self.bookingList.setItemWidget(item, frame)
        else:
            print("Failed to fetch bookings from the API.")

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)
