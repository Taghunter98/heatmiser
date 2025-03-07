import datetime
import time
import unittest
import os
from app.scheduler.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    
    @unittest.skipIf(os.getenv("CI"), "Skipping test in CI pipeline")
    def test_scheduler_runs(self):

        # Simulate current time
        mock_now = datetime.datetime.now()

        # Create scheduler with near-future trigger time
        scheduler = Scheduler(trigger_hour=mock_now.hour, trigger_minute=(mock_now.minute + 1) % 60)

        # Wait for 5 seconds to check if the thread starts
        time.sleep(5)
        
        # Assert that the thread is running
        self.assertTrue(scheduler.running, "Scheduler thread should be running.")

        # Stop the scheduler after the test
        scheduler.stop()
        self.assertFalse(scheduler.running, "Scheduler thread should stop after calling stop().")

if __name__ == "__main__":
    unittest.main()
