import mysql.connector
from dotenv import load_dotenv
import os

def connect():
    # Load variables
    load_dotenv('app/.env')

    try:
        # Set up connection
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
    
def delete(table, fields, values):
    # Set up connection
    connection = connect()
    cursor = connection.cursor()

    # Check parameters
    if fields == 0 or values == 0:
        script = f"DELETE FROM {table};"
    else:
        # Create conditions dynamically
        conditions = [f"{field} = %s" for field in fields]
        condition_string = " AND ".join(conditions)

        # SQL Query
        script = f"DELETE FROM {table} WHERE {condition_string};"

    # Execute the query
    try:
        cursor.execute(script, values)  # Pass the values for placeholders
        connection.commit()
        cursor.close()
        connection.close()
        return "Data deleted successfully"
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return -1