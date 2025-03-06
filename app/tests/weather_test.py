import unittest
from app.weather_api import weather
from app.database import database_setup

class TestDatabase(unittest.TestCase):
    def testCallWeatherApi(self):
        api = weather.WeatherApi('London', 1)
        response = api.callApi()

        # Check JSON data is returned
        self.assertNotEqual(response, -1, "Response data is is not returned as expected.")

    def testParseDataTemp(self):
        api = weather.WeatherApi('London', 1)
        response = api.callApi()
        temp = api.parseDataTemp(response)
        
        # Check data is parsed corectely
        self.assertNotEqual(temp, -1, "Temp data not found in JSON")
        # Check returned object is float
        self.assertIsInstance(temp, float, "Object is not type float")

    def testParseDataTime(self):
        api = weather.WeatherApi('London', 1)
        response = api.callApi()
        time = api.parseDataTime(response)
        
        # Check data is parsed corectely
        self.assertNotEqual(time, -1, "Temp data not found in JSON")
        # Check returned object is string
        self.assertIsInstance(time, str, "Object is not type string")

    def testStoreData(self):
        api = weather.WeatherApi('London', 1)
        data = api.callApi()
        temp = api.parseDataTemp(data)
        time = api.parseDataTime(data)
        store = api.storeData(temp, time)

        self.assertNotEqual(store, -1, "Data is not being stored correcly")

        # Delete text 
        database_setup.delete('TempData', ['mintemp', 'date_added'], [temp, time])

if __name__ == "__main__":
    unittest.main()