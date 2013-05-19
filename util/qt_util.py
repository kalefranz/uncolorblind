from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QCursor, QAction, QMessageBox, QDesktopServices
from functools import partial


def capture_cursor_location():
    pos = QCursor.pos()
    return pos.x(), pos.y()


def format_rgb_string(r, g, b):
    return "{}, {}, {}".format(str(r).rjust(3), str(g).rjust(3), str(b).rjust(3))


def format_coordinate_string(x, y):
    return "{} x {}".format(str(x).rjust(4), str(y).rjust(4))


def bind_menu_bar(window):
    aboutAction = QAction('About', window, triggered=partial(on_about, window))
    websiteAction = QAction('Website', window, triggered=on_website)
    help_menu = window.menuBar().addMenu('Help')
    help_menu.addAction(aboutAction)
    help_menu.addAction(websiteAction)


def on_about(window):
    msg = \
        """
        <center>
        <b><i>uncolorblind</i></b> was developed by<br>
        Kale J. Franz, PhD (<a href="http://www.kalefranz.us">kalefranz.us</a>)<br>
        more at <a href="https://github.com/kalefranz/uncolorblind">github.com/kalefranz/uncolorblind</a>
        </center>
        """
    QMessageBox.about(window, "About uncolorblind ", msg.strip())


def on_website():
    QDesktopServices.openUrl(QUrl("https://github.com/kalefranz/uncolorblind"))