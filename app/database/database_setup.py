import mysql.connector
from dotenv import load_dotenv
import os

def connect():
    # Load variables
    load_dotenv('app/.env')

    try:
        # Establish connection
        connection = mysql.connector.connect(
            host = os.getenv('HOST'),
            user = os.getenv('USER'),
            password = os.getenv('PASS'),
            database = os.getenv('DATABASE')
        )

        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return -1