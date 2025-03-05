import unittest
import requests

class TestFlaskServer(unittest.TestCase):
    def test_server_running(self):
        url = "http://192.168.4.185:6000"
        
        try:
            response = requests.get(url, timeout=5) 
            response.raise_for_status()  
        except requests.exceptions.RequestException as e:
            self.fail(f"Flask server is not running or unreachable: {e}")  
        else:
            self.assertEqual(response.status_code, 200, "Server is running but did not return 200 OK")

if __name__ == "__main__":
    unittest.main()
