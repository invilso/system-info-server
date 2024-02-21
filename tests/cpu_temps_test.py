import unittest
from unittest.mock import MagicMock
from services.cpu import unpack_temperature_data, find_cpu_temperature

class TestTemperatureData(unittest.TestCase):

    def test_unpack_temperature_data(self):
        data = {
            'atk0110': [
                MagicMock(label='CPU Temperature', current=45.0),
                MagicMock(label='MB Temperature', current=35.0)
            ],
            'k10temp': [
                MagicMock(label='', current=31.0)
            ]
        }
        expected_result = {
            'CPU Temperature': 45.0,
            'MB Temperature': 35.0,
            'k10temp_2ae': 31.0
        }
        self.assertEqual(unpack_temperature_data(data), expected_result)

    def test_find_cpu_temperature(self):
        data = {
            'CPU Temp': 50,
            'NB Temp': 40,
            'GPU Temp': 70
        }
        self.assertEqual(find_cpu_temperature(data), 50)

    def test_find_cpu_temperature_no_cpu_temp(self):
        data = {
            'NB Temp': 40,
            'GPU Temp': 70
        }
        self.assertIsNone(find_cpu_temperature(data))

    def test_find_cpu_temperature_empty_data(self):
        data = {}
        self.assertIsNone(find_cpu_temperature(data))

if __name__ == '__main__':
    unittest.main()
