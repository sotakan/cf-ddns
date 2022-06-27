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



class cloudflare:
    def __init__(self) -> None:
        self.token = self.gettoken()
        self.config = self.getconfig()

    def gettoken(self) -> str:
        load_dotenv()
        token = os.getenv("CFDDNS_API_TOKEN")

        if token == None:
            raise Exception("CFDDNS_API_TOKEN not set")

        return f"Bearer {token}"

    def getconfig(self) -> list:
        with open("config.json", "r") as f:
            config = json.load(f)

        return config["records"]

    def getzoneid(self, recordname: str) -> str:
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        params = {"name": recordname}
        zoneid = requests.get("https://api.cloudflare.com/client/v4/zones", headers = headers, params = params).json()
        
        return zoneid["result"][0]["id"]

    def getrecord(self, zoneid: str, subdomain: str) -> str("Dict of: Current IP, Record type, Proxy status, Record ID"):
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        params = {"name": subdomain}
        record = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zoneid}/dns_records", headers = headers, params = params).json()
        
        try:
            return {"content": record["result"][0]["content"], "type": record["result"][0]["type"], "proxy": record["result"][0]["proxied"], "record_id": record["result"][0]["id"]}
        except IndexError:
            return None

    def updaterecord(self, zoneid: str, recordid: str, domain: str, content: str, proxied: bool) -> bool:
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        data = {"name": domain, "type": "A", "proxied": proxied, "content": content, "ttl": 1}
        response = requests.put(f"https://api.cloudflare.com/client/v4/zones/{zoneid}/dns_records/{recordid}", headers = headers, data = json.dumps(data))
        if response.status_code == 200:
            return True
        else:
            return False