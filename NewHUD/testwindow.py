import sys
from PyQt5 import QtWidgets, QtCore

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the minimum width and height
        self.min_width = 700
        self.min_height = 400
        self.bar_height = 60
        self.initial_width = 800
        self.initial_height = 500
        self.name_zones_confirmed = False

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
        self.container.setGeometry(0, 0, self.initial_width, self.initial_height)  # Set the size of the container

        # Create a draggable button
        self.button = QtWidgets.QPushButton("", self.container)
        self.button.move(0, 0)  # Set the initial position of the button
        self.button.resize(self.initial_width, self.bar_height)  # Set the size of the button
        self.button.setStyleSheet("background-color: gray;")

        # Enable drag and drop for the button
        self.button.mousePressEvent = self.button_mouse_press_event
        self.button.mouseMoveEvent = self.button_mouse_move_event

        # Create buttons on the bar
        self.toggle_sidebar_button = QtWidgets.QPushButton("Toggle Sidebar", self.container)
        self.toggle_sidebar_button.move(10, 10)
        self.toggle_sidebar_button.resize(150, 40)
        self.toggle_sidebar_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
        self.toggle_sidebar_button.clicked.connect(self.toggle_sidebar_clicked)

        self.toggle_overlay_button = QtWidgets.QPushButton("Toggle Overlay", self.container)
        self.toggle_overlay_button.move(170, 10)
        self.toggle_overlay_button.resize(150, 40)
        self.toggle_overlay_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
        self.toggle_overlay_button.clicked.connect(self.toggle_overlay_clicked)

        self.edit_name_zones_button = QtWidgets.QPushButton("Edit Name Zones", self.container)
        self.edit_name_zones_button.move(self.initial_width - 280, 10)
        self.edit_name_zones_button.resize(160, 40)
        self.edit_name_zones_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
        self.edit_name_zones_button.clicked.connect(self.edit_name_zones_clicked)

        self.settings_button = QtWidgets.QPushButton("Settings", self.container)
        self.settings_button.move(self.initial_width - 110, 10)
        self.settings_button.resize(100, 40)
        self.settings_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
        self.settings_button.clicked.connect(self.settings_clicked)

        # Create a resize handle (bottom right)
        self.resize_handle_br = QtWidgets.QLabel(self.container)
        self.resize_handle_br.move(self.initial_width - 20, self.initial_height - 20)  # Set the initial position of the resize handle
        self.resize_handle_br.resize(20, 20)  # Set the size of the resize handle
        self.resize_handle_br.setStyleSheet("background-color: gray;")

        # Enable resize for the resize handle (bottom right)
        self.resize_handle_br.mousePressEvent = self.resize_handle_br_mouse_press_event
        self.resize_handle_br.mouseMoveEvent = self.resize_handle_br_mouse_move_event

        # Create a resize handle (bottom left)
        self.resize_handle_bl = QtWidgets.QLabel(self.container)
        self.resize_handle_bl.move(0, self.initial_height - 20)  # Set the initial position of the resize handle
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
            self.button.resize(new_width, self.bar_height)  # Resize the button to match the new width
            self.resize_handle_br.move(new_width - 20, new_height - 20)  # Move the resize handle to the bottom right corner
            self.resize_handle_bl.move(0, new_height - 20)  # Move the resize handle to the bottom left corner
            self.toggle_sidebar_button.move(10, 10)
            self.toggle_overlay_button.move(170, 10)
            self.edit_name_zones_button.move(new_width - 280, 10)
            self.settings_button.move(new_width - 110, 10)

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
            self.button.resize(new_width, self.bar_height)  # Resize the button to match the new width
            self.resize_handle_br.move(new_width - 20, new_height - 20)  # Move the resize handle to the bottom right corner
            self.resize_handle_bl.move(0, new_height - 20)  # Move the resize handle to the bottom left corner
            self.toggle_sidebar_button.move(10, 10)
            self.toggle_overlay_button.move(170, 10)
            self.edit_name_zones_button.move(new_width - 280, 10)
            self.settings_button.move(new_width - 110, 10)

    def toggle_sidebar_clicked(self):
        print("Toggle sidebar clicked")

    def toggle_overlay_clicked(self):
        # For now, take a screenshot
        print("Toggle overlay clicked")
        self.take_screenshot()

    def edit_name_zones_clicked(self):
        if not self.name_zones_confirmed:
            self.toggle_sidebar_button.deleteLater()
            self.toggle_overlay_button.deleteLater()
            self.edit_name_zones_button.deleteLater()
            self.settings_button.deleteLater()

            self.add_name_zone_button = QtWidgets.QPushButton("Add Name Zone", self.container)
            self.add_name_zone_button.move(10, 10)
            self.add_name_zone_button.resize(150, 40)
            self.add_name_zone_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
            self.add_name_zone_button.clicked.connect(self.add_name_zone_clicked)
            self.add_name_zone_button.show()

            self.remove_name_zone_button = QtWidgets.QPushButton("Remove Name Zone", self.container)
            self.remove_name_zone_button.move(170, 10)
            self.remove_name_zone_button.resize(150, 40)
            self.remove_name_zone_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
            self.remove_name_zone_button.clicked.connect(self.remove_name_zone_clicked)
            self.remove_name_zone_button.show()

            self.confirm_button = QtWidgets.QPushButton("Confirm", self.container)
            self.confirm_button.move(self.initial_width - 110, 10)
            self.confirm_button.resize(100, 40)
            self.confirm_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
            self.confirm_button.clicked.connect(self.confirm_clicked)
            self.confirm_button.show()

            self.name_zones_confirmed = True

    def confirm_clicked(self):
        self.add_name_zone_button.deleteLater()
        self.remove_name_zone_button.deleteLater()
        self.confirm_button.deleteLater()

        self.toggle_sidebar_button = QtWidgets.QPushButton("Toggle Sidebar", self.container)
        self.toggle_sidebar_button.move(10, 10)
        self.toggle_sidebar_button.resize(150, 40)
        self.toggle_sidebar_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
        self.toggle_sidebar_button.clicked.connect(self.toggle_sidebar_clicked)
        self.toggle_sidebar_button.show()

        self.toggle_overlay_button = QtWidgets.QPushButton("Toggle Overlay", self.container)
        self.toggle_overlay_button.move(170, 10)
        self.toggle_overlay_button.resize(150, 40)
        self.toggle_overlay_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
        self.toggle_overlay_button.clicked.connect(self.toggle_overlay_clicked)
        self.toggle_overlay_button.show()

        self.edit_name_zones_button = QtWidgets.QPushButton("Edit Name Zones", self.container)
        self.edit_name_zones_button.move(self.initial_width - 280, 10)
        self.edit_name_zones_button.resize(160, 40)
        self.edit_name_zones_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
        self.edit_name_zones_button.clicked.connect(self.edit_name_zones_clicked)
        self.edit_name_zones_button.show()

        self.settings_button = QtWidgets.QPushButton("Settings", self.container)
        self.settings_button.move(self.initial_width - 110, 10)
        self.settings_button.resize(100, 40)
        self.settings_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px;")
        self.settings_button.clicked.connect(self.settings_clicked)
        self.settings_button.show()

        self.name_zones_confirmed = False

    def add_name_zone_clicked(self):
        print("Add name zone clicked")

    def remove_name_zone_clicked(self):
        print("Remove name zone clicked")

    def settings_clicked(self):
        print("Settings clicked")

    def take_screenshot(self):
        screen = QtWidgets.QApplication.screenAt(self.pos())
        screenshot = screen.grabWindow(0, self.x(), self.y(), self.width(), self.height())
        screenshot.save('screenshot.png', 'PNG')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())