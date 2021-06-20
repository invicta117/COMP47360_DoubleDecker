import time
from models.WeatherModel import Base_weather
from scrapper.WeatherScraping import Weather_scrap
from sqlalchemy import create_engine
from dao.CurrentWeatherDao import weather_dao
from dotenv import load_dotenv
import os

local_path = os.path.abspath(os.path.dirname(__file__))
config_path = local_path+"/.env"
load_dotenv(config_path)

# no idea the db URI --- need to be solved
URI = os.getenv("URI")
PORT = "3306"
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")
USER = os.getenv("User") # note: USER will get user name of this computer.


#weather api key
appid=os.getenv("APIKEY_W")
api= os.getenv("API_W")
api_city =os.getenv("API_W_CITY")





# define a method to send a request
def weather_api_city_run(weather_api_obj, dao_weather):
    # Dublin city code : 2964574
    weather_api_obj.sendRequest(2964574)
    # insert rows into RDS
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

            # pause for 10 min
            print("sleep for ten min")
            time.sleep(10 * 60)

        except Exception as e:
            print("something wrong", e)
            time.sleep(1 * 60)

if __name__ == '__main__':
    main()