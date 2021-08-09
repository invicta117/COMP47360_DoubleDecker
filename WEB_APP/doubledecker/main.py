import time
import requests
from sqlalchemy import create_engine
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base
import sys
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


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

Base_weather = declarative_base()

'''create the model to save the data crawling from the Internet'''
class Weather(Base_weather):
    __tablename__ = 'weather'
    lat = Column('lat', Float)
    lon = Column('lon', Float)
    timezone = Column('timezone', String(128))
    current = Column('current', DATETIME, primary_key=True)
    weather_id = Column('weather_id', Integer, primary_key=True)
    weather_icon = Column('weather_icon',String(10))
    visibility = Column('visibility', Float)
    wind_speed = Column('wind_speed', Float)
    wind_deg = Column('wind_deg', Float)
    wind_gust = Column('wind_gust', Float)
    temperature = Column('temperature', Float)
    feels_like = Column('feels_like', Float)
    temp_min = Column('temp_min', Float)
    temp_max = Column('temp_max', Float)
    pressure = Column('pressure', Float)
    humidity = Column('humidity', Float)
    rain_1h = Column('rain_1h', Float)
    snow_1h = Column('snow_1h', Float)
    sunrise = Column('sunrise', DATETIME)
    sunset = Column('sunset', DATETIME)
    description = Column('description', String(100))

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



class weather_dao:
    # init method get engine from variable.
    def __init__(self, engine):
        self.engine = engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    # TODO: filter useful column
    def __filter_Weather_v2(self, arr: dict):
        if 'gust' not in arr['wind']:
            d_gust = 0
        else:
            d_gust = arr['wind']['gust']

        if 'rain' not in arr:
            d_rain = 0
        else:
            d_rain = arr['rain']['rain_1h']
        if 'snow' not in arr:
            d_snow = 0
        else:
            d_snow = arr['snow']['snow_1h']

        return{
            'lat': float(arr["coord"]['lat']),
            'lon': float(arr["coord"]['lon']),
            'timezone': arr['timezone'],
            'current': datetime.datetime.fromtimestamp(arr['dt']),
            'weather_id': int(arr['weather'][0]['id']),
            'weather_icon': arr['weather'][0]['icon'],
            'visibility': arr['visibility'],
            'wind_speed': float(arr['wind']['speed']),
            'wind_deg': float(arr['wind']['deg']),
            'wind_gust': float(d_gust),
            'temperature': float(arr['main']['temp']) - 273,
            'feels_like': float(arr['main']['feels_like']) - 273,
            'temp_min': float(arr['main']['temp_min']) - 273,
            'temp_max': float(arr['main']['temp_max']) - 273,
            'pressure': float(arr['main']['pressure']),
            'humidity': float(arr['main']['humidity']),
            'rain_1h': float(d_rain),
            'snow_1h': float(d_snow),
            'sunrise': datetime.datetime.fromtimestamp(arr['sys']['sunrise']),
            'sunset': datetime.datetime.fromtimestamp(arr['sys']['sunset']),
            'description': arr['weather'][0]['main']
        }

    def insert_weather_to_db(self, weather: dict):
        try:
            weather_column = self.__filter_Weather_v2(weather)
            print('here',weather_column["wind_gust"])
            newWeather = Weather(
                lat=weather_column["lat"],
                lon=weather_column["lon"],
                timezone=weather_column["timezone"],
                current=weather_column["current"],
                weather_id=weather_column["weather_id"],
                weather_icon=weather_column["weather_icon"],
                visibility=weather_column["visibility"],
                wind_speed=weather_column["wind_speed"],
                wind_deg=weather_column["wind_deg"],
                wind_gust=weather_column["wind_gust"],
                temperature=weather_column["temperature"],
                feels_like=weather_column["feels_like"],
                temp_min=weather_column["temp_min"],
                temp_max=weather_column["temp_max"],
                pressure=weather_column["pressure"],
                humidity=weather_column["humidity"],
                rain_1h=weather_column["rain_1h"],
                snow_1h=weather_column["snow_1h"],
                sunrise=weather_column["sunrise"],
                sunset=weather_column["sunset"],
                description=weather_column["description"]
            )
            self.session.add(newWeather)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print('Error message', e)
            pass


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

            # pause for 10 mins
            print("sleep for ten min")
            time.sleep(10 * 60)

        except Exception as e:
            print("something wrong", e)
            time.sleep(1 * 60)


if __name__ == '__main__':
    main()
