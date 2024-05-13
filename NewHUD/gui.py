import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QLabel, QStyle
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QFile, QSettings

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("YourCompany", "YourApp")

        self.folder_path = self.settings.value("folder_path", "")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.logo_label = QLabel()
        pixmap = QPixmap('logo.png')
        self.logo_label.setPixmap(pixmap)
        self.layout.addWidget(self.logo_label)

        self.path_layout = QHBoxLayout()
        self.layout.addLayout(self.path_layout)

        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setToolTip("")
        self.path_input.setText(self.folder_path)
        self.path_layout.addWidget(self.path_input)

        self.button = QPushButton()
        self.button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DirIcon')))
        self.button.clicked.connect(self.open_folder)
        self.path_layout.addWidget(self.button)

    def open_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", self.folder_path)
        self.path_input.setText(self.folder_path)
        self.path_input.setToolTip(self.folder_path)
        self.settings.setValue("folder_path", self.folder_path)
        print("Folder path:", self.folder_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())