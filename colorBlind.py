#!/usr/bin/python

import sys
import numpy as np
from PyQt4.QtCore import SIGNAL, QObject, QTimer, QRect
from PyQt4.QtGui import QApplication, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QWidget, \
    QPixmap, QColor, QCursor, QPainter
from util.util import *

refresh_interval_millis = 75
screen_image_pxs = 160

color_list, rgb_array = create_color_references()


def get_color(r, g, b):
    r_diff = np.absolute(rgb_array[:, 0] - int(r))
    g_diff = np.absolute(rgb_array[:, 1] - int(g))
    b_diff = np.absolute(rgb_array[:, 2] - int(b))
    min_idx = np.argmin(r_diff + g_diff + b_diff)
    return color_list[min_idx]


def capture_screen_area(x, y, width, height):
    return QPixmap.grabWindow(QApplication.desktop().winId(), x, y, width, height).toImage()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('colorBlind')
        self.create_main_frame()
        self.start_timer()

    def create_main_frame(self):
        self.screen_image = QLabel()
        self.screen_image.setFixedSize(screen_image_pxs, screen_image_pxs)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.screen_image)

        rgb_grid = QGridLayout()
        self.color_label = QLabel("Black : Black")
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

    def start_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(refresh_interval_millis)
        QObject.connect(self.timer, SIGNAL('timeout()'), self.update_capture)
        self.timer.start()

    def update_capture(self):
        pos = QCursor.pos()
        x = pos.x()
        y = pos.y()
        self.x_coord_label.setText(str(x))
        self.y_coord_label.setText(str(y))

        image = capture_screen_area(x-5, y-5, 15, 15)
        color = QColor(image.pixel(7, 7))
        (r, g, b) = (color.red(), color.green(), color.blue())

        scaled_pixmap = QPixmap.fromImage(image.scaled(screen_image_pxs, screen_image_pxs))
        painter = QPainter()
        painter.begin(scaled_pixmap)
        painter.drawRect(QRect(80-5, 80-5, 10, 10))
        painter.drawRect(QRect(0, 0, 159, 159))
        painter.end()

        self.screen_image.setPixmap(scaled_pixmap)
        self.r_dec_label.setText(str(r))
        self.g_dec_label.setText(str(g))
        self.b_dec_label.setText(str(b))

        color = get_color(r, g, b)
        self.color_label.setText("{0} : {1}".format(color['group'], color['name']))
        self.rgb_hex_label.setText("#{}".format(rgb_to_hex(r, g, b)))


def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    form.raise_()
    app.exec_()


main()