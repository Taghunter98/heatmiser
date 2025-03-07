import requests
from app.database import database_setup
import mysql.connector
import datetime

class WeatherApi():
    def __init__(self, postcode, days):
        self.postcode = postcode
        self.days = days
        pass

    def weatherApi(self):
        # Get the current time
        cur_time = datetime.datetime.now()

        # Call function only if the current time is midnight
        if self.checkTime(cur_time.hour) != -1:
            data = self.callApi()
            temp = self.parseDataTemp(data)
            time = self.parseDataTime(data)
            self.storeData(temp, time)
            return 1
        else:
            return -1

    def callApi(self):
        
        URL = f'http://api.weatherapi.com/v1/forecast.json?key=ac2509f894e84d20b84193300250503&q={self.postcode}&days={self.days}&aqi=no&alerts=no'
    
        try:
            request = requests.get(url = URL)
            data = request.json()
            return data
        except Exception as e:
            print(f"Error: {e}")
        return -1
    
    def parseDataTemp(self, data):
        min_temp = data["forecast"]["forecastday"][0]["day"]["mintemp_c"]
        if min_temp is None:
            return -1
        else:
            return min_temp
        
    def parseDataTime(self, data):
        time = data["current"]["last_updated"]
        if time is None:
            return -1
        else:
            return time
        
    def storeData(self, min_temp, time):
        try:
            # Send data to database
            connection = database_setup.connect()
            cursor = connection.cursor()
            script = f"INSERT INTO TempData (mintemp, date_added) VALUES ({min_temp}, '{time}');"
            cursor.execute(script)
            connection.commit()
            cursor.close()
            connection.close()
            return "Data stored successfully"
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return -1
        
    def checkTime(self, time):
        # Check if the time is midnight
        if time == 0:
            return time
        else:
            return -1
        