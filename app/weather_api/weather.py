import requests
from app.database import database_setup
import mysql.connector
import logging

# Set up logging in heating.log
logging.basicConfig(
    filename="heating.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class WeatherApi():
    """
    This class fetches, stores and returns real time weather data
    
    """

    def __init__(self, postcode, days):
        """ 
        Creates the WeatherApi object

        Args:
            postcode (string): The postcode for weather data
            days (int): The number of days to gather data
        """

        self.postcode = postcode
        self.days = days
        pass

    def weatherApi(self):
        """
        Method to fetch the minimum temperature, store result in the database and return temperature

        Returns:
            float: The minimum temperature in the 24 hour period
        """

        data = self.callApi()
        if data == -1:
            logging.error("API call failed. Cannot fetch weather data.")
            return None
        
        temp = self.parseDataTemp(data)
        time = self.parseDataTime(data)
        self.storeData(temp, time)
            
        result = database_setup.retrieve("TempData", ["mintemp", "date_added"], [temp, time])

        if result:
            min_temp = result[0]["mintemp"]
            logging.info(f"Retrieved min temperature from database: {min_temp}°C")
            return min_temp
        else:
            logging.warning("No temperature data found in database.")
            return None

    def callApi(self):
        """
        Method to call the api from weatherapi.com

        Returns:
            float: The minimum temperature from the returned JSON
        """
        
        URL = f'http://api.weatherapi.com/v1/forecast.json?key=ac2509f894e84d20b84193300250503&q={self.postcode}&days={self.days}&aqi=no&alerts=no'
    
        try:
            logging.info(f"Making API request to {URL}")
            request = requests.get(url=URL)
            request.raise_for_status()
            data = request.json()
            logging.info("API request successful.")
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            return -1
    
    def parseDataTemp(self, data):
        """
        Method to parse the temperature from JSON

        Args:
            data (JSON): The JSON returned from the weather api

        Returns:
            float: minimum temperature in the 24 period
        """

        min_temp = data["forecast"]["forecastday"][0]["day"]["mintemp_c"]
        if min_temp is None:
            return -1
        else:
            return min_temp
        
    def parseDataTime(self, data):
        """
        Method to parse the date and time from JSON

        Args:
            data (JSON): The JSON returned from the weather api

        Returns:
            string: The date and time of the api call
        """

        time = data["current"]["last_updated"]
        if time is None:
            return -1
        else:
            return time
        
    def storeData(self, min_temp, time):
        """
        Method to store data in the MySQL database

        Args:
            min_temp (float): The minimum temperature in the 24 hour period
            time (string): The date and time of the api call

        Returns:
            string: Success message or -1 if error occurs
        """

        try:
            connection = database_setup.connect()
            cursor = connection.cursor()
            script = f"INSERT INTO TempData (mintemp, date_added) VALUES ({min_temp}, '{time}');"
            cursor.execute(script)
            connection.commit()
            cursor.close()
            connection.close()

            logging.info(f"Stored temperature data: {min_temp}°C at {time}")
            return "Data stored successfully"
        except mysql.connector.Error as e:
            logging.error(f"Database error: {e}")
            return -1