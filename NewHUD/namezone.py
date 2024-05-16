from PyQt5 import QtWidgets, QtCore
import sys

class NameZone(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.5); border: 1px solid black;")
        self.setGeometry(10, 60, 100, 50)  # Initial position and size
        self.show()

        self.x = 10
        self.y = 60
        self.width = 100
        self.height = 50

    def mousePressEvent(self, event):
        self.drag_start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.pos() + self.pos() - self.drag_start_pos)
            self.x = self.x()  # Update x coordinate
            self.y = self.y()  # Update y coordinate

    def resizeEvent(self, event):
        self.resize_handle_br.move(self.width() - 20, self.height() - 20)
        self.width = self.width()  # Update width
        self.height = self.height()  # Update height

    def add_resize_handles(self):
        self.resize_handle_br = QtWidgets.QLabel(self)
        self.resize_handle_br.move(self.width - 20, self.height - 20)
        self.resize_handle_br.resize(20, 20)
        self.resize_handle_br.setStyleSheet("background-color: gray;")

        self.resize_handle_br.mousePressEvent = self.resize_handle_br_mouse_press_event
        self.resize_handle_br.mouseMoveEvent = self.resize_handle_br_mouse_move_event

    def resize_handle_br_mouse_press_event(self, event):
        self.resize_start_pos = event.globalPos()
        self.resize_start_width = self.width
        self.resize_start_height = self.height

    def resize_handle_br_mouse_move_event(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            delta = event.globalPos() - self.resize_start_pos
            new_width = max(self.resize_start_width + delta.x(), 20)
            new_height = max(self.resize_start_height + delta.y(), 20)
            self.resize(new_width, new_height)
            self.width = new_width  # Update width
            self.height = new_height  # Update height