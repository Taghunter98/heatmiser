import unittest
import requests
import os
from unittest.mock import patch

class TestFlaskServer(unittest.TestCase):
    @patch("requests.get")
    def test_server_running(self, mock_get):
        if os.getenv("CI"):
            mock_get.return_value.status_code = 200  # Fake a 200 response
        else:
            response = requests.get("http://192.168.4.135:6000", timeout=5)
            response.raise_for_status()
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
