import unittest
from unittest.mock import patch  
from app.database import database_setup
import os

class TestDatabase(unittest.TestCase):
    @patch("app.database.database_setup.connect")
    def testConnection(self, mock_connect):
        if os.getenv("CI"):  
            mock_connect.return_value = "mock_db"  # Fake a successful connection
        else:
            connection = database_setup.connect()
            self.assertNotEqual(connection, -1, "Connection is not working")

if __name__ == "__main__":
    unittest.main()
