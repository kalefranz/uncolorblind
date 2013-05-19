import unittest
import sys
import re
from PyQt4.QtCore import Qt, QEvent
from PyQt4.QtGui import QApplication, QKeyEvent, QHideEvent, QShowEvent, QCloseEvent
from uncolorblind import MainWindow


class TestMainApp(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

    def tearDown(self):
        """
        For some reason, the python interpreter crashes on final exit from this test suite. It has to be something
        with PyQt (tearDown or tearDownClass) that I'm not doing right.  Hints welcome!
        """
        self.app.quit()

    def test_initialization(self):
        self.assertTrue(self.main_window.timer.isActive())

    def test_freeze_unfreeze_on_space_bar(self):
        space_bar_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Space, Qt.NoModifier)
        self.main_window.keyPressEvent(space_bar_event)
        self.assertFalse(self.main_window.timer.isActive())
        self.main_window.keyPressEvent(space_bar_event)
        self.assertTrue(self.main_window.timer.isActive())

    def test_copy_hex_on_enter(self):
        QApplication.clipboard().clear()
        self.assertEqual("", QApplication.clipboard().text())
        enter_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier)
        self.main_window.keyPressEvent(enter_event)
        current_clipboard = QApplication.clipboard().text()
        match = re.search("#[0-9]{6}", current_clipboard)
        self.assertIsNotNone(match)

    def test_freeze_on_minimize_then_unfreeze_maximize(self):
        self.main_window.hideEvent(QHideEvent.Hide)
        self.assertFalse(self.main_window.timer.isActive())
        self.main_window.showEvent(QShowEvent.Show)
        self.assertTrue(self.main_window.timer.isActive())


if __name__ == '__main__':
    unittest.main()