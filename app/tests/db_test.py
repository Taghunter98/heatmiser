import unittest
from app.database import database_setup

class TestDatabase(unittest.TestCase):
    def testConnection(self):
        connection = database_setup.connect()
        self.assertNotEqual(connection, -1)

if __name__ == "__main__":
    unittest.main()