import json
import unittest
import os
import sys

from entities.die import Die
from entities.quad import Quad
from utils.constants import *


class TestDie(unittest.TestCase):

    def setUp(self):
        # נתוני דמה ליצירת מחלקת Die
        with open("../data/chip_data.json", 'r') as config:
            chip_data = json.load(config)

        die_data = chip_data.get(TOP, {}).get(DIES, [])[0]
        self.die = Die(1, die_data)

    def test_initialization(self):
        # בדיקה שהמחלקה נבנית כראוי
        self.assertEqual(self.die.id, 1)
        self.assertEqual(self.die.type_name, DIE)
        self.assertFalse(self.die.is_enable)
        self.assertEqual(len(self.die.quads), 2)  # נוודא שיש 2 שורות בקואדים

    def test_init_quads(self):
        # בדיקה שה-quads מאותחלים בצורה נכונה
        quads_matrix = self.die.quads

        # בדיקה שכל שורה מכילה 2 עמודות
        self.assertEqual(len(quads_matrix[0]), 2)
        self.assertEqual(len(quads_matrix[1]), 2)

        # בדיקה שהאובייקטים מסוג Quad נוצרו כהלכה
        self.assertIsInstance(quads_matrix[0][0], Quad)
        self.assertIsInstance(quads_matrix[1][1], Quad)

        # בדיקה שה-quads תואמים לנתונים שסיפקנו
        self.assertEqual(quads_matrix[0][0].id, 1)
        self.assertEqual(quads_matrix[1][1].id, 4)

    def test_get_attribute_from_active_logs(self):
        mock_attribute = 'some_attribute'
        attributes = self.die.get_attribute_from_active_logs(mock_attribute)

        self.assertIsInstance(attributes, list)

if __name__ == '__main__':
    unittest.main()
