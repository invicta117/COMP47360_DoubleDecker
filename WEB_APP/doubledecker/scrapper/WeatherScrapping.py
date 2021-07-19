import requests
import json
import sys
import os


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

class Weather_scrap:

    def __init__(self, api, appid):
        self._api = api
        self._appid = appid
        self._request = None
        self.weather = None
        self.city = "Dublin"

    # request city weather
    def sendRequest(self,id):
        try:
            self._request = requests.get(self._api, params={"appid": self._appid, "id": id})
            print(self._request.url)
            print(json.loads(self._request.text))
            self.weather = self._request.json()
        except:
            print("send request fail: ", self._request)