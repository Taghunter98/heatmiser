from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Scheduler import for setting up the recipes
from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.scheduler import scheduler_bp, Scheduler

scheduler = BackgroundScheduler()

def create_app():
    """
    Function to build the Flask application

    Raises:
        ValueError: If the secret key is missing.

    Returns:
        object: Flask app object
    """

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins='*')

    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')

    if not secret_key:
        raise ValueError("Error: SECRET_KEY is missing from environment variables")
    
    app.config.from_mapping(
        SECRET_KEY=secret_key
    )

    # Register blueprints for API calls
    app.register_blueprint(scheduler_bp)

    @app.route('/')
    def home():
        return "Server is running", 200

    if not scheduler.running:
        scheduler.add_job(Scheduler(app).run, "cron", hour=0, minute=0)
        scheduler.start()

    return app
