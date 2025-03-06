import unittest
from app.database import database_setup

class TestDatabase(unittest.TestCase):
    def testConnection(self):
        connection = database_setup.connect()
        # Check connection, if wrong it will return -1
        self.assertNotEqual(connection, -1, "Connection is not working")

if __name__ == "__main__":
    unittest.main()