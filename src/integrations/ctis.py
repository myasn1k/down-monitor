import requests
from datetime import datetime, timedelta

class CTIS():

    headers = {}
    url = ""

    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.CTIS_login(username, password)

    def do_get(self, url):
        return requests.get(self.url + url, headers=self.headers).json()
    
    def do_post(self, url, json):
        return requests.post(self.url + url, headers=self.headers, json=json).json()

    def get_operations_and_urls(self, op_label, delta_seconds):
        start_date = datetime.utcnow() - timedelta(seconds=delta_seconds)
        json = {
                 "where": {
                     "labels": {
                         "$in": [
                             "ddos"
                         ]
                     },
                     "_created": {
                         "$gte": start_date.strftime("%Y-%m-%d %H:%M:%SZ")
                     }
                 }
            }
        ops = self.do_post("/x-operations/get?page=1&max_results=25", json)["_items"]
        res = {}
        for op in ops:
            rels = self.do_get("/urls/relationships/x-operations/"+op['_id'])
            res[op["name"]] = []
            for rel in rels['_items']:
                res[op["name"]].append(rel['value'])
        return res

    def CTIS_login(self, user, password):
        #response = requests.post(f"{self.url}/api/auth/login", json={"username": user, "password": password})
        response = requests.get(f"{self.url}/login", auth=(user, password))
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + response.json()["data"]["access_token"]}
