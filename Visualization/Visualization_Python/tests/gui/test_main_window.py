import unittest
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from utols.data_manager import DataManager

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Visualization_Python')))

class TestMainWindow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # יצירת מופע של QApplication עבור בדיקות PyQt
        cls.app = QApplication([])

    def setUp(self):
        # יצירת מופע של DataManager ו MainWindow
        self.data_manager = DataManager('data/chip_data.json', 'sl.json')
        self.main_window = MainWindow(self.data_manager)

    def test_initialization(self):
        # בדוק את אתחול ה-UI
        self.assertEqual(self.main_window.windowTitle(), 'HW simulator')
        self.assertEqual(self.main_window.geometry().width(), 800)
        self.assertEqual(self.main_window.geometry().height(), 600)

    def test_load_dies(self):
        # בדוק שהדאטה של DIEs נטענה כראוי
        self.assertIn(0, self.main_window.dies)
        self.assertIn(1, self.main_window.dies)

    def test_create_navbar(self):
        # בדוק את יצירת ה-navbar ואת הפעולות שלו
        menu_bar = self.main_window.menuBar()
        self.assertIsNotNone(menu_bar)
        self.assertTrue(menu_bar.actions())





    def test_clear_content(self):
        # בדוק שהתוכן נמחק כראוי
        self.main_window.show_die1()
        self.main_window.clear_content()
        # Verify the die_widget is removed from the layout
        self.assertEqual(self.main_window.scroll_content_layout.count(), 0)

    @classmethod
    def tearDownClass(cls):
        # סגור את QApplication לאחר הבדיקות
        cls.app.quit()

# if __name__ == '__main__':
#     unittest.main()
