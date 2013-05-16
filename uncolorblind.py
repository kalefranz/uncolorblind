#!/usr/bin/python

import os
import sys
from PyQt4.QtCore import SIGNAL, QObject, QTimer, QRect
from PyQt4.QtGui import QApplication, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QWidget
from color_util import get_color, rgb_to_hex
from image_util import capture_cursor_location, capture_screen_area, calculate_px_rgb, prepare_pixmap


class Constants(object):
    """
    This class is meant to add an easy way to dynamically scale zoom, center area size, etc
    """
    def __init__(self):
        self.refresh_interval_millis = 75
        self.mouse_offset = -5
        self.display_image_pxs = 140
        self.capture_image_pxs = 15
        self.sub_image_pxs = 10
        self.set_dependent_values()

    def set_dependent_values(self):
        self.sub_image_anchor_px = self.display_image_pxs / 2 - self.sub_image_pxs / 2
        self.display_image_edge_pxs = self.display_image_pxs - 1

c = Constants()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.create_main_frame()
        self.start_polling()

    def create_main_frame(self):
        self.setWindowTitle(os.path.basename(__file__).strip(".py"))
        self.screen_image = QLabel()
        self.screen_image.setFixedSize(c.display_image_pxs, c.display_image_pxs)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.screen_image)

        rgb_grid = QGridLayout()
        self.color_label = QLabel(" ")
        self.r_dec_label = QLabel("0")
        self.g_dec_label = QLabel("0")
        self.b_dec_label = QLabel("0")
        self.rgb_hex_label = QLabel("#0000000")
        self.x_coord_label = QLabel("0")
        self.y_coord_label = QLabel("0")
        rgb_grid.addWidget(self.color_label, 0,0, 1,3)
        rgb_grid.addWidget(QLabel("R"), 1,0, 1,1)
        rgb_grid.addWidget(QLabel("G"), 1,1, 1,1)
        rgb_grid.addWidget(QLabel("B"), 1,2, 1,1)
        rgb_grid.addWidget(self.r_dec_label, 2,0, 1,1)
        rgb_grid.addWidget(self.g_dec_label, 2,1, 1,1)
        rgb_grid.addWidget(self.b_dec_label, 2,2, 1,1)
        rgb_grid.addWidget(self.rgb_hex_label, 3,0, 1,3)
        rgb_grid.addWidget(self.x_coord_label, 4,0, 1,3)
        rgb_grid.addWidget(self.y_coord_label, 4,1, 1,3)
        mainLayout.addLayout(rgb_grid)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(mainLayout)
        self.setCentralWidget(self.mainWidget)

    def start_polling(self):
        self.timer = QTimer()
        self.timer.setInterval(c.refresh_interval_millis)
        QObject.connect(self.timer, SIGNAL('timeout()'), self.update_capture)
        self.timer.start()

    def update_capture(self):
        x, y = capture_cursor_location()
        self.x_coord_label.setText(str(x))
        self.y_coord_label.setText(str(y))

        original_capture_image = capture_screen_area(x + c.mouse_offset, y + c.mouse_offset,
                                                     c.capture_image_pxs, c.capture_image_pxs)
        scaled_image = original_capture_image.scaled(c.display_image_pxs, c.display_image_pxs)
        sub_image = scaled_image.copy(QRect(c.sub_image_anchor_px, c.sub_image_anchor_px,
                                            c.sub_image_pxs, c.sub_image_pxs))
        r, g, b = calculate_px_rgb(sub_image, c.sub_image_pxs)

        self.screen_image.setPixmap(prepare_pixmap(scaled_image, c))
        self.r_dec_label.setText(str(r))
        self.g_dec_label.setText(str(g))
        self.b_dec_label.setText(str(b))

        color = get_color(r, g, b)
        self.color_label.setText("<b>{0}</b><br>{1}".format(color['name'], color['group']))
        self.rgb_hex_label.setText("#{0}".format(rgb_to_hex(r, g, b)))


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    form.raise_()
    app.exec_()

if __name__ == "__main__":
    main()