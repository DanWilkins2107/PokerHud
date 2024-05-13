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

        # Create a resize handle
        self.resize_handle = QtWidgets.QLabel(self.container)
        self.resize_handle.move(280, 180)  # Set the initial position of the resize handle
        self.resize_handle.resize(20, 20)  # Set the size of the resize handle
        self.resize_handle.setStyleSheet("background-color: gray;")

        # Draw a triangle in the resize handle
        pixmap = QtGui.QPixmap(20, 20)
        pixmap.fill(QtGui.QColor("transparent"))
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
        painter.setBrush(QtGui.QBrush(QtGui.QColor("gray")))
        painter.drawPolygon(QtGui.QPolygon([QtCore.QPoint(10, 0), QtCore.QPoint(20, 20), QtCore.QPoint(0, 20)]))
        painter.end()
        self.resize_handle.setPixmap(pixmap)

        # Enable resize for the resize handle
        self.resize_handle.mousePressEvent = self.resize_handle_mouse_press_event
        self.resize_handle.mouseMoveEvent = self.resize_handle_mouse_move_event

    def button_mouse_press_event(self, event):
        self.drag_start_pos = event.pos()

    def button_mouse_move_event(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_pos)

    def resize_handle_mouse_press_event(self, event):
        self.resize_start_pos = event.globalPos()
        self.resize_start_width = self.width()
        self.resize_start_height = self.height()

    def resize_handle_mouse_move_event(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            delta = event.globalPos() - self.resize_start_pos
            new_width = max(self.resize_start_width + delta.x(), 200)  # Minimum width is 200
            new_height = max(self.resize_start_height + delta.y(), 100)  # Minimum height is 100
            self.resize(new_width, new_height)
            self.container.resize(new_width, new_height)
            self.resize_handle.move(new_width - 20, new_height - 20)  # Move the resize handle to the bottom right corner

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())