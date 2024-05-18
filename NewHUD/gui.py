import sys
import os
from PIL import Image
from imagehash import phash
from PyQt5 import QtWidgets, QtCore
import re
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the minimum width and height
        self.min_width = 700
        self.min_height = 400
        self.bar_height = 60
        self.initial_width = 800
        self.initial_height = 500

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

        self.name_zones = []
        self.name_zone_labels = []
        self.name_zone_images = {}

        self.name_zone_editing = False
        self.active_name_zone = 0
        self.remove_name_zone_on_release = False
        self.default_name_zone_size = {'width': 20, 'height': 10}

        self.images_changed = False
        self.name_strings = []

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

            # Update positions of all buttons
            self.toggle_sidebar_button.move(10, 10)
            self.toggle_overlay_button.move(170, 10)
            self.edit_name_zones_button.move(new_width - 280, 10)
            self.settings_button.move(new_width - 110, 10)

            self.add_name_zone_button.move(10, 10)
            self.remove_name_zone_button.move(170, 10)
            self.confirm_button.move(new_width - 110, 10)
            self.update_name_zones()

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

            # Update positions of all buttons
            self.toggle_sidebar_button.move(10, 10)
            self.toggle_overlay_button.move(170, 10)
            self.edit_name_zones_button.move(new_width - 280, 10)
            self.settings_button.move(new_width - 110, 10)

            self.add_name_zone_button.move(10, 10)
            self.remove_name_zone_button.move(170, 10)
            self.confirm_button.move(new_width - 110, 10)

            self.update_name_zones()

    def toggle_sidebar_clicked(self):
        # For now, print namestrings
        print(self.name_strings)

    def toggle_overlay_clicked(self):
        # For now, take a screenshot
        print("Toggle overlay clicked")
        self.take_screenshot()

    def edit_name_zones_clicked(self):
        self.toggle_sidebar_button.hide()
        self.toggle_overlay_button.hide()
        self.edit_name_zones_button.hide()
        self.settings_button.hide()

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

        self.container.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border: 2px solid black;")

        self.name_zone_editing = True
        for label in self.name_zone_labels:
            label.show()

    def confirm_clicked(self):
        self.add_name_zone_button.hide()
        self.remove_name_zone_button.hide()
        self.confirm_button.hide()

        for label in self.name_zone_labels:
            label.hide()

        self.container.setStyleSheet("background-color: transparent; border: 2px solid black;")

        self.name_zone_editing = False

        self.toggle_sidebar_button.show()
        self.toggle_overlay_button.show()
        self.edit_name_zones_button.show()
        self.settings_button.show()

    def add_name_zone_clicked(self):
        name_zone = {
            'x': 0,  # Relative x position (5%)
            'y': 0,  # Relative y position (15%)
            'width': self.default_name_zone_size['width'],  # Relative width
            'height': self.default_name_zone_size['height']  # Relative height
        }
        self.name_zones.append(name_zone)
        self.update_name_zones()
        self.active_name_zone = len(self.name_zones) - 1
        self.update_name_zones()
        print(self.name_zones)

    def remove_name_zone_clicked(self):
        if self.name_zones:
            del self.name_zones[self.active_name_zone]
            self.active_name_zone = len(self.name_zones) - 1
            self.update_name_zones()
        
    def update_name_zones(self):
        for label in self.name_zone_labels:
            label.deleteLater()
        self.name_zone_labels = []

        for i, name_zone in enumerate(self.name_zones):
            sectionHeight = self.container.height() - self.bar_height
            x = int((name_zone['x'] / 100) * self.container.width())
            y = int((name_zone['y'] / 100) * sectionHeight + self.bar_height) 
            width = int((name_zone['width'] / 100) * self.container.width())
            height = int((name_zone['height'] / 100) * sectionHeight)

            label = QtWidgets.QLabel(self.container)
            label.setGeometry(x, y, width, height)
            if i == self.active_name_zone:
                label.setStyleSheet("background-color: rgba(0, 255, 0, 0.7); border: 2px solid rgb(0, 0, 0);")
            else:
                label.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border: 2px solid rgb(0, 0, 0);")
            if self.name_zone_editing:
                label.show()
            self.name_zone_labels.append(label)

            label.mousePressEvent = lambda event, label=label: self.label_mouse_press_event(event, label)
            label.mouseMoveEvent = lambda event, label=label: self.label_mouse_move_event(event, label)
            label.mouseReleaseEvent = lambda event, label=label: self.label_mouse_release_event(event, label)

            # Create a resize handle for the label
            resize_handle = QtWidgets.QLabel(label)
            resize_handle.move(width - 20, height - 20)
            resize_handle.resize(20, 20)
            resize_handle.setStyleSheet("background-color: gray;")
            resize_handle.show()

            # Enable resize for the resize handle
            resize_handle.mousePressEvent = lambda event, label=label, resize_handle=resize_handle: self.resize_handle_mouse_press_event(event, label, resize_handle)
            resize_handle.mouseMoveEvent = lambda event, label=label, resize_handle=resize_handle: self.resize_handle_mouse_move_event(event, label, resize_handle)

    def resize_handle_mouse_press_event(self, event, label, resize_handle):
        self.resize_start_pos = event.globalPos()
        self.resize_start_width = label.width()
        self.resize_start_height = label.height()

    def resize_handle_mouse_move_event(self, event, label, resize_handle):
        if event.buttons() == QtCore.Qt.LeftButton:
            delta = event.globalPos() - self.resize_start_pos
            new_width = max(self.resize_start_width + delta.x(), 20)  # Minimum width is 20
            new_height = max(self.resize_start_height + delta.y(), 20)  # Minimum height is 20
            label.resize(new_width, new_height)
            resize_handle.move(new_width - 20, new_height - 20)

            for i, name_zone in enumerate(self.name_zones):
                if self.name_zone_labels[i] == label:
                    section_height = self.container.height() - self.bar_height
                    self.name_zones[i]['width'] = (new_width / self.container.width()) * 100
                    self.name_zones[i]['height'] = (new_height / section_height) * 100
                    self.default_name_zone_size['width'] = (new_width / self.container.width()) * 100
                    self.default_name_zone_size['height'] = (new_height / section_height) * 100

    def label_mouse_press_event(self, event, label):
        self.drag_start_pos = event.pos()
        self.drag_label = label
        self.active_name_zone = self.name_zone_labels.index(label)

    def label_mouse_move_event(self, event, label):
        if event.buttons() == QtCore.Qt.LeftButton:
            delta = event.pos() - self.drag_start_pos
            new_x = self.drag_label.x() + delta.x()
            new_y = self.drag_label.y() + delta.y()
            self.drag_label.move(new_x, new_y)

            for i, name_zone in enumerate(self.name_zones):
                if self.name_zone_labels[i] == self.drag_label:
                    self.name_zones[i]['x'] = (new_x / self.container.width()) * 100
                    self.name_zones[i]['y'] = ((new_y - self.bar_height) / (self.container.height() - self.bar_height)) * 100 

                    if new_x < 0 or new_y < self.bar_height or self.name_zones[i]['x'] + name_zone['width'] > 100 or self.name_zones[i]['y'] + name_zone['height'] > 100:
                        self.remove_name_zone_on_release = True
                        return
                    self.remove_name_zone_on_release = False
                

    def label_mouse_release_event(self, event, label):
        if self.remove_name_zone_on_release:
            self.name_zones.pop(self.active_name_zone)
            self.active_name_zone = len(self.name_zones) - 1
        self.remove_name_zone_on_release = False
        self.update_name_zones()

    def settings_clicked(self):
        print("Settings clicked")

    def take_screenshot(self):
        screen = QtWidgets.QApplication.screenAt(self.pos())
        screenshot = screen.grabWindow(0, self.x(), self.y(), self.width(), self.height())

        for i, name_zone in enumerate(self.name_zones):
            x = int((name_zone['x'] / 100) * self.container.width())
            y = int((name_zone['y'] / 100) * (self.container.height() - self.bar_height)) + self.bar_height
            width = int((name_zone['width'] / 100) * self.container.width())
            height = int((name_zone['height'] / 100) * (self.container.height() - self.bar_height))

            cropped_screenshot = screenshot.copy(x, y, width, height)

            if not os.path.exists('images'):
                os.makedirs('images')

            filename = f'images/namezone_{i+1}.png'
            cropped_screenshot.save(filename, 'PNG')

            img_hash = phash(Image.open(filename))
            if i in self.name_zone_images:
                if self.name_zone_images[i] != img_hash:
                    self.image_changed(i)
                    self.images_changed = True
            else:
                self.image_added(i)
                self.images_changed = True

            self.name_zone_images[i] = img_hash

        # Remove any images where the namezone no longer exists
        for filename in os.listdir('images'):
            match = re.match(r'namezone_(\d+)\.png', filename)
            if match:
                index = int(match.group(1)) - 1
                if index >= len(self.name_zones):
                    os.remove(os.path.join('images', filename))
                    self.image_removed(index)
            else:
                os.remove(os.path.join('images', filename))

        if self.images_changed:
            print("Images changed")
            self.run_tesseract()
            self.images_changed = False

    def run_tesseract(self):
        self.name_strings = []
        for i in range(len(self.name_zones)):
            filename = f'images/namezone_{i+1}.png'
            img = Image.open(filename)
            text = pytesseract.image_to_string(img)
            self.name_strings.append(text.strip())

    def image_changed(self, index):
            print(f"Image {index + 1} changed")

    def image_added(self, index):
            print(f"Image {index + 1} added")

    def image_removed(self, index):
            print(f"Image {index + 1} removed")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())