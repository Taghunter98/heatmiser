from flask import Flask, jsonify
import unittest
import os
from app.scheduler.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    
    @unittest.skipIf(os.getenv("CI"), "Skipping test in CI pipeline")
    def test_scheduler_runs(self):
        # Create a Flask app context to test the function that uses jsonify
        app = Flask(__name__)
        
        with app.app_context():
            # Instantiate Scheduler and call the run method
            api = Scheduler()
            job = api.run()

            # Check that the response has a 200 status code
            self.assertEqual(job.status_code, 200, "Expected status code 200")

            # Parse JSON response
            json_response = job.get_json()

            # Check that the 'status' key in the response is 'success'
            self.assertEqual(json_response.get("status"), "success", "API call is not working as expected")

if __name__ == "__main__":
    unittest.main()
