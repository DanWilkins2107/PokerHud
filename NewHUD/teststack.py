import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.title_bar = QLabel(self)
        self.title_bar.setGeometry(0, 0, self.width(), 30)
        self.title_bar.setStyleSheet("background-color: rgba(255, 255, 255, 0.7);")
        self.title_bar.setText("EASYPOKERHUD")

        self.close_button = QPushButton(self.title_bar)
        self.close_button.setGeometry(self.title_bar.width() - 20, 0, 20, 20)
        self.close_button.setText("X")
        self.close_button.clicked.connect(app.quit)
        self.close_button.raise_()

        self.content_area = QWidget(self)
        self.content_area.setGeometry(0, 30, self.width(), self.height() - 30)
        self.content_area.setWindowFlags(Qt.WindowTransparentForInput | Qt.SubWindow)
        self.content_area.setAttribute(Qt.WA_TranslucentBackground)
        self.content_area.setStyleSheet("background-color: transparent;")

        self.pushButton = QPushButton(self.content_area)
        self.pushButton.setGeometry(QRect(240, 190, 90, 31))
        self.pushButton.setText("Finished")
        self.pushButton.clicked.connect(app.quit)

        self.dragging = False
        self.drag_pos = QPoint()

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.7)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.white))   
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.title_bar.underMouse():
            self.dragging = True
            self.drag_pos = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.dragging = False

app = QApplication(sys.argv)

# Create the main window
window = CustomWindow()
window.resize(500, 300)

# Run the application
window.show()
sys.exit(app.exec_())