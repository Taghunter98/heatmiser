import datetime
from flask import Blueprint, jsonify
from app.weather_api import weather
from app.commands.commands import Command

# Create a Blueprint
scheduler_bp = Blueprint("scheduler_bp", __name__)

class Scheduler:
    def run(self):
        print(f"Running scheduled Recipe at {datetime.datetime.now()}")

        # Fetch, store and retrieve weather API
        api = weather.WeatherApi('TN174HH', 1)
        min_temp = api.weatherApi()

        # Set up Recipe
        try:
            recipe = Command("wss://192.168.4.174:4243", "0e0df290-8821-4de8-b14a-45cd3b83c33f")
            print("Connected to Heatmiser Neo")

            # Check temperature and run Recipe based on it
            if min_temp > 9:
                recipe.runRecipe("6am Start Time.")
                return jsonify({"status": "success", "message": "Running 6am Heating Start Recipe..."})
            elif min_temp > 5:
                recipe.runRecipe("4.30 am Heating Start")
                return jsonify({"status": "success", "message": "Running 4:30am Heating Start Recipe..."})
            elif min_temp > 1:
                recipe.runRecipe("3.30am Heating Start.")
                return jsonify({"status": "success", "message": "Running 3:30am Heating Start Recipe..."})
            elif min_temp > -3:
                recipe.runRecipe("2am Heating Start.")
                return jsonify({"status": "success", "message": "Running 2am Heating Start Recipe..."})
            else:
                return jsonify({"status": "error", "message": "Temperature out of range."})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

# Define an API endpoint to trigger the scheduler
@scheduler_bp.route("/run", methods=["POST"])
def run_schedule():
    scheduler = Scheduler()
    return scheduler.run()
