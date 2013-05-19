#!/usr/bin/python

import os
import sys
from PyQt4.QtCore import SIGNAL, QObject, QTimer, QRect, Qt
from PyQt4.QtGui import QApplication, QHBoxLayout, QLabel, QMainWindow, QWidget, QIcon, QVBoxLayout
from util.color_util import get_color, rgb_to_hex
from util.image_util import capture_screen_area, calculate_px_rgb, prepare_pixmap
from util.qt_util import capture_cursor_location, bind_menu_bar, format_rgb_string, format_coordinate_string
from constants import Constants


app_name = os.path.basename(__file__).strip(".py")
c = Constants()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.create_main_frame()
        self.init_polling()

    def create_main_frame(self):
        self.setWindowTitle(app_name)
        self.screen_image = QLabel()
        self.screen_image.setFixedSize(c.display_image_pxs, c.display_image_pxs)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.screen_image)

        # variable display fields
        self.color_label_primary = QLabel("<b>Black</b>")
        self.color_label_group = QLabel("Gray Scale")
        self.rgb_dec_label = QLabel(format_rgb_string(0, 0, 0))
        self.rgb_hex_label = QLabel("#0000000")
        self.mouse_coords_label = QLabel("0 x 0")

        # font setup
        font_10pt = QLabel().font()
        font_10pt.setPointSize(10)
        font_12pt = QLabel().font()
        font_12pt.setPointSize(12)
        font_14pt = QLabel().font()
        font_14pt.setPointSize(14)
        font_14pt.setBold(True)
        self.color_label_primary.setFont(font_14pt)
        self.color_label_group.setFont(font_12pt)

        # information box layout
        info_box_layout = QVBoxLayout()
        info_box_layout.setSpacing(0)
        info_box_layout.setMargin(0)
        info_box_layout.setContentsMargins(0, 0, 0, 0)
        color_name_layout = QHBoxLayout()
        color_name_layout.addWidget(self.color_label_primary, 0, Qt.AlignLeft)
        color_name_layout.addWidget(self.color_label_group, 0, Qt.AlignRight)
        info_box_layout.addLayout(color_name_layout)
        info_box_layout.itemAt(info_box_layout.count() - 1).layout().setContentsMargins(0, 0, 0, 15)
        rgb_dec_layout = QHBoxLayout()
        rgb_dec_layout.addWidget(QLabel("<b>RGB:  </b>"))
        rgb_dec_layout.addWidget(self.rgb_dec_label, Qt.AlignLeft)
        info_box_layout.addLayout(rgb_dec_layout)
        info_box_layout.addWidget(QLabel('<font color="darkGray"><b><i>C</i></b> to copy to clipboard</font>'),
                                  0, Qt.AlignRight)
        info_box_layout.itemAt(info_box_layout.count() - 1).widget().setFont(font_10pt)
        rgb_hex_layout = QHBoxLayout()
        rgb_hex_layout.addWidget(QLabel("<b>Hex:  </b>"))
        rgb_hex_layout.addWidget(self.rgb_hex_label, Qt.AlignLeft)
        info_box_layout.addLayout(rgb_hex_layout)
        info_box_layout.addWidget(QLabel('<font color="darkGray"><b><i>Enter</i></b> to copy to clipboard</font>'),
                                  0, Qt.AlignRight)
        info_box_layout.itemAt(info_box_layout.count() - 1).widget().setFont(font_10pt)
        mouse_coords_layout = QHBoxLayout()
        mouse_coords_layout.addWidget(QLabel("<b>coords: </b>"))
        mouse_coords_layout.addWidget(self.mouse_coords_label, Qt.AlignLeft)
        info_box_layout.addLayout(mouse_coords_layout)
        info_box_layout.addWidget(QLabel('<font color="darkGray"><b><i>Space Bar</i></b> to freeze</font>'),
                                  0, Qt.AlignRight)
        info_box_layout.itemAt(info_box_layout.count() - 1).widget().setFont(font_10pt)
        mainLayout.addLayout(info_box_layout)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.setFixedSize(c.window_width, c.window_height)

    def init_polling(self):
        self.timer = QTimer()
        self.timer.setInterval(c.refresh_interval_millis)
        QObject.connect(self.timer, SIGNAL('timeout()'), self.update_capture)
        self.timer.start()
        self.timer_was_active = True

    def hideEvent(self, QHideEvent):
        self.timer_was_active = self.timer.isActive()
        self.timer.stop()

    def showEvent(self, QShowEvent):
        if self.timer_was_active:
            self.timer.start()

    def keyPressEvent(self, QKeyEvent):
        key = QKeyEvent.key()
        if key == Qt.Key_Space:  # space bar
            self.toggle_polling()
        elif key in (Qt.Key_Return, Qt.Key_Enter):  # enter key
            self.copy_hex()

    def toggle_polling(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()

    def copy_hex(self):
        QApplication.clipboard().setText(self.rgb_hex_label.text())

    def update_capture(self):
        x, y = capture_cursor_location()
        self.mouse_coords_label.setText(format_coordinate_string(x, y))

        original_capture_image = capture_screen_area(x + c.mouse_offset, y + c.mouse_offset,
                                                     c.capture_image_pxs, c.capture_image_pxs)
        scaled_image = original_capture_image.scaled(c.display_image_pxs, c.display_image_pxs)
        sub_image = scaled_image.copy(QRect(c.sub_image_anchor_px, c.sub_image_anchor_px,
                                            c.sub_image_pxs, c.sub_image_pxs))
        r, g, b = calculate_px_rgb(sub_image, c.sub_image_pxs)

        self.screen_image.setPixmap(prepare_pixmap(scaled_image, c))
        self.rgb_dec_label.setText(format_rgb_string(r, g, b))

        color = get_color(r, g, b)
        self.color_label_primary.setText(color['name'])
        self.color_label_group.setText(color['group'])
        self.rgb_hex_label.setText("#{}".format(rgb_to_hex(r, g, b)))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(app_name)
    app.setWindowIcon(QIcon('aux/apple_rainbow.png'))

    main_window = MainWindow()
    bind_menu_bar(main_window)
    main_window.show()
    main_window.raise_()
    app.exec_()

if __name__ == "__main__":
    main()