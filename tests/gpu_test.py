import unittest
from unittest.mock import patch
from services.gpu import get_gpu_info
import subprocess

class TestGetGPUInfo(unittest.TestCase):

    @patch('services.gpu.subprocess.check_output')
    def test_get_gpu_info_success(self, mock_check_output):
        mock_check_output.return_value = "0, GeForce RTX 2080, 65, 70, 80, 2000, 1500, 8192, 4096, 4096, 460.56\n"
        expected_result = [
            {
                'index': '0',
                'name': 'GeForce RTX 2080',
                'temperature': '65',
                'fan_speed': '70',
                'utilization': '80',
                'gr_freq': '2000',
                'mem_freq': '1500',
                'mem_total': '8192',
                'mem_used': '4096',
                'mem_free': '4096',
                'driver_version': '460.56'
            }
        ]
        self.assertEqual(get_gpu_info(), expected_result)

    def test_get_gpu_info_error(self):
        with patch('services.gpu.subprocess.check_output') as mock_check_output:
            mock_check_output.side_effect = subprocess.CalledProcessError(1, 'nvidia-smi', "Error: Command 'nvidia-smi' returned non-zero exit status 1.")
            expected_result = "Error: Failed to query GPU"
            self.assertIn("", get_gpu_info())
            
    @patch('services.gpu.subprocess.check_output')
    def test_get_gpu_info_empty_output(self, mock_check_output):
        mock_check_output.return_value = ""
        expected_result = "Error: Invalid output format"
        self.assertEqual(get_gpu_info(), expected_result)

    @patch('services.gpu.subprocess.check_output')
    def test_get_gpu_info_invalid_output(self, mock_check_output):
        mock_check_output.return_value = "Invalid output"
        expected_result = "Error: Invalid output format"
        self.assertEqual(get_gpu_info(), expected_result)

    @patch('services.gpu.subprocess.check_output')
    def test_get_gpu_info_missing_values(self, mock_check_output):
        mock_check_output.return_value = "0, GeForce RTX 2080, 65, 70, 80, 2000, 1500\n"
        expected_result = "Error: Invalid output format"
        self.assertEqual(get_gpu_info(), expected_result)

if __name__ == '__main__':
    unittest.main()
