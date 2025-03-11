from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

# Scheduler import for setting up the recipes
from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.scheduler import scheduler_bp, Scheduler

# Setup logging to file
logging.basicConfig(
    filename="heating.log", 
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

scheduler = BackgroundScheduler()

def create_app():
    """
    Function to build the Flask application

    Raises:
        ValueError: If the secret key is missing.

    Returns:
        object: Flask app object
    """
    logging.debug("Starting Flask app...")

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins='*')

    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')

    if not secret_key:
        logging.error("Error: SECRET_KEY is missing from environment variables")
        raise ValueError("Error: SECRET_KEY is missing from environment variables")
    
    app.config.from_mapping(SECRET_KEY=secret_key)

    # Register blueprints for API calls
    app.register_blueprint(scheduler_bp)

    @app.route('/')
    def home():
        return "Server is running", 200

    logging.debug("Checking scheduler status...")

    try:
        if not scheduler.running:
            logging.debug("Scheduler is not running, adding job...")
            scheduler.add_job(Scheduler(app).run, "cron", hour=0, minute=0)
            scheduler.start()
            logging.debug("Scheduler started successfully.")
        else:
            logging.debug("Scheduler is already running.")
    except Exception as e:
        logging.error(f"Error starting scheduler: {e}")

    return app