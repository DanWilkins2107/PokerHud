import sys
from PyQt5 import QtWidgets, QtCore

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the minimum width and height
        self.min_width = 400
        self.min_height = 300

        # Make the window frameless and transparent
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint  # Removes the window frame
            | QtCore.Qt.Tool  # Hides the taskbar icon
            | QtCore.Qt.WindowStaysOnTopHint  # Always keeps the window on top
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Makes the background transparent

        # Create a main container widget
        self.container = QtWidgets.QWidget(self)
        self.container.setStyleSheet("background-color: transparent; border: 2px solid black;")
        self.container.setGeometry(0, 0, 300, 200)  # Set the size of the container

        # Create a draggable button
        self.button = QtWidgets.QPushButton("Drag me!", self.container)
        self.button.move(0, 0)  # Set the initial position of the button
        self.button.resize(300, 30)  # Set the size of the button
        self.button.setStyleSheet("background-color: gray;")

        # Enable drag and drop for the button
        self.button.mousePressEvent = self.button_mouse_press_event
        self.button.mouseMoveEvent = self.button_mouse_move_event

        # Create a resize handle (bottom right)
        self.resize_handle_br = QtWidgets.QLabel(self.container)
        self.resize_handle_br.move(280, 180)  # Set the initial position of the resize handle
        self.resize_handle_br.resize(20, 20)  # Set the size of the resize handle
        self.resize_handle_br.setStyleSheet("background-color: gray;")

        # Enable resize for the resize handle (bottom right)
        self.resize_handle_br.mousePressEvent = self.resize_handle_br_mouse_press_event
        self.resize_handle_br.mouseMoveEvent = self.resize_handle_br_mouse_move_event

        # Create a resize handle (bottom left)
        self.resize_handle_bl = QtWidgets.QLabel(self.container)
        self.resize_handle_bl.move(0, 180)  # Set the initial position of the resize handle
        self.resize_handle_bl.resize(20, 20)  # Set the size of the resize handle
        self.resize_handle_bl.setStyleSheet("background-color: gray;")

        # Enable resize for the resize handle (bottom left)
        self.resize_handle_bl.mousePressEvent = self.resize_handle_bl_mouse_press_event
        self.resize_handle_bl.mouseMoveEvent = self.resize_handle_bl_mouse_move_event

    def button_mouse_press_event(self, event):
        self.drag_start_pos = event.pos()

    def button_mouse_move_event(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_pos)

    def resize_handle_br_mouse_press_event(self, event):
        self.resize_start_pos = event.globalPos()
        self.resize_start_width = self.width()
        self.resize_start_height = self.height()

    def resize_handle_br_mouse_move_event(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            delta = event.globalPos() - self.resize_start_pos
            new_width = max(self.resize_start_width + delta.x(), self.min_width)
            new_height = max(self.resize_start_height + delta.y(), self.min_height)
            self.resize(new_width, new_height)
            self.container.resize(new_width, new_height)
            self.button.resize(new_width, 30)  # Resize the button to match the new width
            self.resize_handle_br.move(new_width - 20, new_height - 20)  # Move the resize handle to the bottom right corner
            self.resize_handle_bl.move(0, new_height - 20)  # Move the resize handle to the bottom left corner

    def resize_handle_bl_mouse_press_event(self, event):
        self.resize_start_pos = event.globalPos()
        self.resize_start_width = self.width()
        self.resize_start_height = self.height()
        self.resize_start_x = self.x()

    def resize_handle_bl_mouse_move_event(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            delta = event.globalPos() - self.resize_start_pos
            old_width = self.width()
            new_width = max(self.resize_start_width - delta.x(), self.min_width)
            new_height = max(self.resize_start_height + delta.y(), self.min_height)
            self.move(self.x() + (old_width - new_width), self.y())
            self.resize(new_width, new_height)
            self.container.resize(new_width, new_height)
            self.button.resize(new_width, 30)  # Resize the button to match the new width
            self.resize_handle_br.move(new_width - 20, new_height - 20)  # Move the resize handle to the bottom right corner
            self.resize_handle_bl.move(0, new_height - 20)  # Move the resize handle to the bottom left corner


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())