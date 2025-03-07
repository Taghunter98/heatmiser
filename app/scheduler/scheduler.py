import sched
import datetime
import threading
import time

class Scheduler():
    def __init__(self, trigger_hour=0, trigger_minute=0):
        # Creates the scheduler with modular time
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.trigger_hour = trigger_hour
        self.trigger_minute = trigger_minute
        self.running = True
        self.thread = None
        self.scheduleNextRecipe()
    
    def runRecipe(self):
        print(f"Running scheduled Recipe at {datetime.datetime.now()}")

        # Fetch, store and retrieve weather API
        # Check temperature and run Recipe based on it

        # Schedule next Recipe
        self.scheduleNextRecipe()

    def scheduleNextRecipe(self):
        # Schedules the next Recipe at the specified trigger time.
        now = datetime.datetime.now()
        next_run = datetime.datetime.combine(now.date(), datetime.time(self.trigger_hour, self.trigger_minute))

        # If the scheduled time for today has passed, schedule for tomorrow
        if now > next_run:
            next_run += datetime.timedelta(days=1)

        delay = (next_run - now).total_seconds()
        print(f"Next run scheduled in {delay} seconds (at {next_run}).")

        self.scheduler.enter(delay, 1, self.runRecipe)

        # Run the scheduler in a separate thread 
        threading.Thread(target=self.scheduler.run, daemon=True).start()

        # For debugging 
        print(f"Active Threads: {threading.enumerate()}")

    def stop(self):
        print("Stopping scheduler...")
        self.running = False 
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
        print("Scheduler stopped.")