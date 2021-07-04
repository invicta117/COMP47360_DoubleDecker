import time
from modelLevel.WeatherModel import Base_weather
import requests
from sqlalchemy import create_engine
from dao.CurrentWeatherDao import weather_dao
import json
import os

# no idea the db URI --- need to be solved
URI = "localhost"
PORT = "3306"
PASSWORD = "123"
DB = "gtfs"
USER = "student"  # note: USER will get user name of this computer.

# weather api key
appid = "92fb08f48a98e0f39b990060352ffebe"
api = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
api_city = "https://api.openweathermap.org/data/2.5/weather"


class Weather_scrap:

    def __init__(self, api, appid):
        self._api = api
        self._appid = appid
        self._request = None
        self.weather = None
        self.city = "Dublin"

    # request city weather
    def sendRequest(self, id):
        try:
            self._request = requests.get(self._api, params={"appid": self._appid, "id": id})
            print(self._request.url)
            print(json.loads(self._request.text))
            self.weather = self._request.json()
        except:
            print("send request fail: ", self._request)


# define a method to send a request
def weather_api_city_run(weather_api_obj, dao_weather):
    # Dublin city code : 2964574
    weather_api_obj.sendRequest(2964574)
    # insert rows into Database

    dao_weather.insert_weather_to_db(weather_api_obj.weather)


def main():
    # create engine
    engine = create_engine(
        "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

    # create weather table in RDS
    Base_weather.metadata.create_all(engine)

    # create dao obj
    dao_weather = weather_dao(engine)

    # create api obj
    weather_api_obj = Weather_scrap(api_city, appid)

    # TODO: add some log record function.
    while True:
        try:
            print("restart")
            # request JCD stations data
            weather_api_city_run(weather_api_obj, dao_weather)

            # pause for 1 h
            print("sleep for ten min")
            time.sleep(10 * 60)

        except Exception as e:
            print("something wrong", e)
            time.sleep(1 * 60)


if __name__ == '__main__':
    main()
