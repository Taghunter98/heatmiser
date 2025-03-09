from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.scheduler import scheduler_bp, Scheduler

from app.scheduler.scheduler import scheduler_bp

def create_app():
    # Create and configure application
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins='*')

    # Get key
    load_dotenv()

    # Run application only if secret key is provided
    secret_key = os.getenv('SECRET_KEY')

    if not secret_key:
        raise ValueError("Error: SECRET_KEY is messing from environment variables")
    app.config.from_mapping(
        SECRET_KEY = secret_key
    )

    # Register scheduler
    app.register_blueprint(scheduler_bp)

    @app.route('/')
    def home():
        return "Server is running", 200
    
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(Scheduler(app).run, "cron", hour=0, minute=0)
    scheduler.start()

    return app