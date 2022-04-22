import json
import requests

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

