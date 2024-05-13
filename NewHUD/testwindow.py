import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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
        button = QtWidgets.QPushButton("Drag me!", self.container)
        button.move(0, 0)  # Set the initial position of the button
        button.resize(300, 30)  # Set the size of the button
        button.setStyleSheet("background-color: gray;")

        # Enable drag and drop for the button
        button.mousePressEvent = self.button_mouse_press_event
        button.mouseMoveEvent = self.button_mouse_move_event

    def button_mouse_press_event(self, event):
        self.drag_start_pos = event.pos()

    def button_mouse_move_event(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_pos)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())