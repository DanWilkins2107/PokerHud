import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

        # Custom title bar
        self.title_bar = QWidget(self)
        self.title_bar.setFixedSize(400, 30)
        self.title_bar.setStyleSheet("background: rgba(0, 0, 0, 100);")  # Semi-transparent black
        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        # Title Label
        title = QLabel("Custom Title Bar", self.title_bar)
        self.title_bar_layout.addWidget(title)

        # Close Button
        close_button = QPushButton("X", self.title_bar)
        close_button.clicked.connect(app.quit)
        self.title_bar_layout.addWidget(close_button)

        # Enable dragging
        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return
        delta = QPoint(event.globalPos() - self.old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

app = QApplication(sys.argv)
window = CustomWindow()
window.resize(400, 200)
window.show()
sys.exit(app.exec_())