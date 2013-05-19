import numpy as np
from PyQt4.QtCore import QRect
from PyQt4.QtGui import QApplication, QPixmap, QColor, QPainter


def capture_screen_area(x, y, width, height):
    return QPixmap.grabWindow(QApplication.desktop().winId(), x, y, width, height).toImage()


def calculate_px_rgb(sub_image, xy_length):
    """
    I hate that this function uses a double for loop
    Any way to just map a full QImage to numpy array???
    """
    px_tot = np.zeros(3)
    for x in xrange(xy_length):
        for y in xrange(xy_length):
            color = QColor(sub_image.pixel(x, y))
            px_tot += (color.red(), color.green(), color.blue())
    avg_rgb = (px_tot / float(sub_image.width() * sub_image.height())).astype(np.int16)
    return avg_rgb[0], avg_rgb[1], avg_rgb[2]


def prepare_pixmap(image, c):
    pixmap = QPixmap.fromImage(image)
    painter = QPainter()
    painter.begin(pixmap)
    painter.drawRect(QRect(c.sub_image_anchor_px, c.sub_image_anchor_px,
                           c.sub_image_pxs, c.sub_image_pxs))  # draw center square
    painter.drawRect(QRect(0, 0, c.display_image_edge_pxs, c.display_image_edge_pxs))  # draw border
    painter.end()
    return pixmap
