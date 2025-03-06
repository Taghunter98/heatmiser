import mysql.connector
from dotenv import load_dotenv
import os

def connect():
    # Get variables
    load_dotenv('app/.env')

    try:
        # Establish connection
        database = mysql.connector.connect(
            host = os.getenv('HOST'),
            user = os.getenv('USER'),
            password = os.getenv('PASS'),
            database = os.getenv('DATABASE')
        )
        print("Connection is successful")
        return database
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return -1
    
connect()