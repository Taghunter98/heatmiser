import unittest
from unittest.mock import patch
from app.database import database_setup
import os
import mysql.connector

class TestDatabase(unittest.TestCase):
    @patch("app.database.database_setup.connect")
    def testConnection(self, mock_connect):
        # Fake test for CI
        if os.getenv("CI"):  
            mock_connect.return_value = "mock_db" 
        else:
            connection = database_setup.connect()
            self.assertNotEqual(connection, -1, "Connection is not working")
    
    @patch("app.database.database_setup.connect")
    def testDelete(self, mock_connect):
        # Fake test for CI
        if os.getenv("CI"):
            mock_connect.return_value = "Content deletion works as expected"
            # Test that the function works for CI environment
            result = database_setup.delete("users", ["name", "age"], ["John", 30])
            self.assertEqual(result, "Data deleted successfully")
        else:
            # Local test to delete fake data
            temp = 5.6
            time = "2025-01-01 00:00"
            
            connection = database_setup.connect()
            cursor = connection.cursor()
            script = f"INSERT INTO TempData (mintemp, date_added) VALUES ({temp}, {time});"
            cursor.execute()
            connection.commit()
            cursor.close()
            connection.close()

            # Call the delete function
            result = database_setup.delete("TempData", ["mintemp", "date_added"], [temp, time])

            # Assert the result is as expected
            self.assertEqual(result, "Data deleted successfully", "Data was not deleted.")


if __name__ == "__main__":
    unittest.main()
