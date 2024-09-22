import unittest
from data_manager import DataManager
from log import Log

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager('data/chip_data.json', 'sl.json')

    def test_load_json(self):
        chip_data = self.data_manager.load_json('data/chip_data.json')
        sl_data = self.data_manager.load_json('data/sl.json')
        self.assertIsInstance(chip_data, dict)
        self.assertIsInstance(sl_data, dict)

    def test_parse_logs(self):
        logs = self.data_manager.parse_logs()
        self.assertIsInstance(logs, list)
        self.assertTrue(all(isinstance(log, Log) for log in logs))

    def test_get_start_time(self):
        start_time = self.data_manager.get_start_time()
        self.assertIsNotNone(start_time)

    def test_get_end_time(self):
        end_time = self.data_manager.get_end_time()
        self.assertIsNotNone(end_time)

    def test_enable_die(self):
        self.data_manager.load_die(0)
        self.data_manager.load_die(1)
        self.data_manager.enable_die()
        self.assertTrue(any(die.is_enable for die in self.data_manager.die_objects.values()))

# if __name__ == '__main__':
#     unittest.main()
