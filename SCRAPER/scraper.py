import os
import requests
import json
import mysql.connector
import datetime
import time

WEATHERUSER = os.environ["WEATHERUSER"]
DBPASS = os.environ["DBPASS"]
APIKEY_W = os.environ["APIKEY_W"]


class scraper():

    def get_data(self, lat=53.3498, lon=-6.2603):
        """Get the data from open weather maps api return as txt format"""
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid=92fb08f48a98e0f39b990060352ffebe")
        return r.text

    def get_columns(self, current):
        """get individual data columns from data"""
        columns = {"dt": "NULL", "temp": "NULL", "pressure": "NULL", "humidity": "NULL", "dew_point": "NULL", "rain": 0}

        try:
            date = datetime.datetime.fromtimestamp(current["dt"])
            columns["dt"] = date.strftime("%Y/%m/%d %H:%M:%S")
        except Exception as e:
            print("Error with date", e)

        try:
            C = current["temp"] - 273.15
            columns["temp"] = C
        except Exception as e:
            print("Error with temp", e)

        try:
            columns["pressure"] = current["pressure"]
        except Exception as e:
            print("Error with pressure", e)

        try:
            columns["humidity"] = current["humidity"]
        except Exception as e:
            print("Error with humidity", e)

        try:
            columns["dew_point"] = current["dew_point"]
        except Exception as e:
            print("Error with dew_point", e)

        try:
            columns["rain"] = current["rain"]["1h"]
        except Exception as e:
            # expect that rain will not be there often due to nature of data
            pass

        return tuple(columns.values())

    def process_data(self, data):
        """Process the json data and place it into the database"""
        parsed = json.loads(data)
        current = parsed["current"]
        future = parsed["hourly"]
        current_res = self.get_columns(current)
        self.database_conn("current", -1, current_res)
        for hour, data in enumerate(future):
            current_res = self.get_columns(data)
            self.database_conn("current", hour, current_res)

    def database_conn(self, table, hr, data):
        """Create database connection and sql statement for placing data into database"""
        # origionally from https://www.w3schools.com/python/python_mysql_insert.asp
        mydb = mysql.connector.connect(
            host="localhost",
            user=WEATHERUSER,
            password=DBPASS,
            database="weather"
        )
        mycursor = mydb.cursor()
        sql = f"UPDATE weather.{table} SET hr = {hr}, dt = %s, temp = %s, pressure = %s, humidity = %s, dewpoint = %s, rain = %s where hr = {hr}"
        mycursor.execute(sql, data)
        mydb.commit()

    def run(self, mins=15):
        """method to put run the entire scraper"""
        attempts = 0
        while True:
            try:
                data = self.get_data()
                self.process_data(data)
                attempts = 0
                time.sleep(mins * 60)
            except Exception as e:
                print(e)
                attempts += 1
                if attempts > 5:
                    print("Persistent Error quitting", datetime.now())
                    break
                time.sleep(1 * 60)
                print("Error at", datetime.datetime.now())


if __name__ == "__main__":
    s = scraper()
    s.run()
