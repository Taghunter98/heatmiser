import mysql.connector
from dotenv import load_dotenv
import os

def connect():
    """
    Function to connect to the MySQL database

    Returns:
        connection: Databse connection object
    """

    load_dotenv('app/.env')

    try:
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
    """
    Function to delete from the database

    Args:
        table (string): The database table to delete from
        fields (array): The fields in the table
        values (array): The values to delete

    Returns:
        string: Success message or -1 if error
    """
    
    connection = connect()
    cursor = connection.cursor()

    if fields == 0 or values == 0:
        script = f"DELETE FROM {table};"
    else:
        conditions = [f"{field} = %s" for field in fields]
        condition_string = " AND ".join(conditions)
        
        script = f"DELETE FROM {table} WHERE {condition_string};"

    try:
        cursor.execute(script, values)  
        connection.commit()
        cursor.close()
        connection.close()

        return "Data deleted successfully"
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return -1
    
def retrieve(table, fields, values):
    """
    Function to retrieve from MySQL database

    Args:
        table (string): The database table to delete from
        fields (array): The fields in the table
        values (array): The values to add

    Returns:
        string: Success message or -1 if error
    """

    
    connection = connect()
    cursor = connection.cursor(dictionary=True) 

    if not fields or not values:
        script = f"SELECT * FROM {table};"
        params = ()
    else:
        conditions = [f"{field} = %s" for field in fields]
        condition_string = " AND ".join(conditions)

        script = f"SELECT * FROM {table} WHERE {condition_string};"
        params = values

    try:
        cursor.execute(script, params)  
        results = cursor.fetchall()  
        cursor.close()
        connection.close()
        
        return results
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return -1