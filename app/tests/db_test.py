import unittest
from unittest.mock import patch
from app.database import database_setup
import os

class TestDatabase(unittest.TestCase):
    @unittest.skipIf(os.getenv("CI"), "Skipping test in CI pipeline")
    def testConnection(self):

        # Setup connection
        connection = database_setup.connect()

        # Check connection is returned
        self.assertNotEqual(connection, -1, "Connection is not working")
    
    @unittest.skipIf(os.getenv("CI"), "Skipping test in CI pipeline")
    def testDelete(self):
        
        # Local test to delete fake data
        temp = 5.6
        time = "2025-01-01 00:00"
        
        connection = database_setup.connect()
        cursor = connection.cursor()
        script = f"INSERT INTO TempData (mintemp, date_added) VALUES ({temp}, '{time}');"
        cursor.execute(script)
        connection.commit()
        cursor.close()
        connection.close()

        # Call the delete function
        result = database_setup.delete("TempData", ["mintemp", "date_added"], [temp, time])

        # Assert the result is as expected
        self.assertEqual(result, "Data deleted successfully", "Data was not deleted.")

    @unittest.skipIf(os.getenv("CI"), "Skipping test in CI pipeline")
    def testRetrieve(self):
        # Local test to insert fake data
        temp = 5.6
        time = "2025-01-01 00:00"

        connection = database_setup.connect()
        cursor = connection.cursor()
    
        # Insert test data
        script = f"INSERT INTO TempData (mintemp, date_added) VALUES ({temp}, '{time}');"
        cursor.execute(script)
        connection.commit()
        cursor.close()
        connection.close()

        # Call the retrieve function
        result = database_setup.retrieve("TempData", ["mintemp", "date_added"], [temp, time])

        # Assert the retrieved data matches inserted data
        self.assertTrue(len(result) > 0, "No data retrieved.")
        self.assertEqual(result[0]["mintemp"], temp, "Retrieved temperature does not match.")
        self.assertEqual(result[0]["date_added"], time, "Retrieved date does not match.")

        # Cleanup: Delete the test entry
        database_setup.delete("TempData", ["mintemp", "date_added"], [temp, time])




if __name__ == "__main__":
    unittest.main()
