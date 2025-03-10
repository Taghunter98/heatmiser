import datetime
from flask import Blueprint, jsonify
import logging
from dotenv import load_dotenv
import os

# Modules
from app.weather_api import weather
from app.commands.commands import Command

# Email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create a Blueprint
scheduler_bp = Blueprint("scheduler_bp", __name__)

# Set up logging in heating.log
logging.basicConfig(
    filename="heating.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Scheduler:
    """
    This class runs a Recipe on the Heatmiser Neo

    """

    def __init__(self, app):
        """
        Creates the Scheduler object

        Args:
        app (object): The flask application onject
        """
        self.app = app
    
    def sendEmail(self, message):
        """
        Method to send an email to the client

        Args:
            message (string): The message body of the email
        """

        # Email Configuration
        load_dotenv('app/.env')
        EMAIL_SENDER = os.getenv('EMAIL_SENDER')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
        EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')
        
        try:
            msg = MIMEMultipart()
            msg['From'] = "Heatmiser Automation" 
            msg['To'] = EMAIL_RECEIVER
            msg['Subject'] = "Heating Recipe Triggered"

            # Attach message body
            msg.attach(MIMEText(message, 'plain'))

            # Connect to the SMTP server
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        
                logging.info(f"Email notification sent: {message}")
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")


    def run(self):
        """
        Method to run a Recipe

        Returns:
            JSON: JSON containing either success or error for api
        """

        with self.app.app_context():
            logging.info(f"Running scheduled Recipe at {datetime.datetime.now()}")

            # Fetch, store and retrieve weather API
            logging.info("Fetching weather data...")
            try:
                api = weather.WeatherApi('TN174HH', 1)
                min_temp = api.weatherApi()
                email_temp = f"\n\n24 hour minimum temperature is {min_temp}°C"
                logging.info(f"24 hour minimum temperature is {min_temp}°C")
            except Exception as e:
                logging.error(f"Error: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500

            # Set up Recipe
            try:
                recipe = Command("wss://192.168.4.174:4243", "0e0df290-8821-4de8-b14a-45cd3b83c33f")
                logging.info("Connected to Heatmiser Neo")

                # Check temperature and run Recipe based on it
                if min_temp > 9:
                    message = "Heatmiser Neo is running 6am Heating Start Recipe..."
                    recipe.runRecipe("6am Start Time.")
                elif min_temp > 5:
                    message = "Heatmiser Neo is running 4:30am Heating Start Recipe..."
                    recipe.runRecipe("4.30 am Heating Start")
                elif min_temp > 1:
                    message = "Heatmiser Neo is running 3:30am Heating Start Recipe..."
                    recipe.runRecipe("3.30am Heating Start.")
                elif min_temp > -3:
                    message = "Heatmiser Neo is running 2am Heating Start Recipe..."
                    recipe.runRecipe("2am Heating Start.")
                else:
                    message = "Temperature out of range. No heating started."
                    logging.warning(message)
                    return jsonify({"status": "error", "message": message}), 400

                # Log and send email 
                logging.info(message)
                self.sendEmail((message + email_temp))

                return jsonify({"status": "success", "message": message})

            except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint to run a Recipe
@scheduler_bp.route("/run", methods=["POST"])
def run_schedule():
    """
    API endpoint for running a Recipe manually

    Returns:
        JSON: JSON containing either success or error for api
    """

    from flask import current_app
    scheduler = Scheduler(current_app)
    result = scheduler.run()

    # Check if the schedule returns a result for email
    if result:
        return result
    return jsonify({"status": "error", "message": "No result returned from scheduler."}), 500