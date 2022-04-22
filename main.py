import json
import requests
import os
from dotenv import load_dotenv

class ip:
    def getcurrentip(self) -> str:
        ip = requests.get("https://api.ipify.org?format=json").json()
        return ip["ip"]

    def updatepersist(self, current: str):
        with open("ippresist.json", "w") as f:
            json.dump({"previousip": current}, f)

    def getpreviousip(self) -> str:
        try:
            with open("ippresist.json", "r") as f:
                ip = json.load(f)
        except FileNotFoundError:
            return None
        
        return ip["previousip"]

def getconfig() -> list:
    with open("config.json", "r") as f:
        config = json.load(f)

    return config["records"]

def gettoken() -> str:
    load_dotenv()
    token = os.getenv("CFDDNS_API_TOKEN")

    if token == None:
        raise Exception("CFDDNS_API_TOKEN not set")

    return token

