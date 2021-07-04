import time
from modelLevel.WeatherModel import Base_weather
from scrapper.WeatherScraping import Weather_scrap
from sqlalchemy import create_engine
from dao.CurrentWeatherDao import weather_dao
from dotenv import load_dotenv
import os

local_path = os.path.abspath(os.path.dirname(__file__))
config_path = local_path+"/.env"
load_dotenv(config_path)

# no idea the db URI --- need to be solved
URI = "localhost"
PORT = "3306"
PASSWORD = ""
DB = ""
USER = "" # note: USER will get user name of this computer.


#weather api key
appid="92fb08f48a98e0f39b990060352ffebe"
api="https://api.openweathermap.org/data/2.5/onecall/timemachine"
api_city = "https://api.openweathermap.org/data/2.5/weather"





# define a method to send a request
def weather_api_city_run(weather_api_obj, dao_weather):
    # Dublin city code : 2964574
    weather_api_obj.sendRequest(2964574)
    # insert rows into Database
    
    dao_weather.insert_weather_to_db(weather_api_obj.weather)


def main():
    # create engine
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

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
            weather_api_city_run(weather_api_obj,dao_weather)

            # pause for 1 h
            print("sleep for ten min")
            time.sleep(60 * 60)

        except Exception as e:
            print("something wrong", e)
            time.sleep(1 * 60)

if __name__ == '__main__':
    main()