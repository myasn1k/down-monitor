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
                             op_label
                         ]
                     },
                     "first_seen": {
                         "$gte": start_date.strftime("%Y-%m-%d %H:%M:%SZ")
                     }
                 }
            }

        ops = []
        page = 1
        while True:
            tmp = self.do_post(f"/x-operations/get?page={page}&max_results=25", json)["_items"]
            if not tmp:
                break
            ops += tmp
            page += 1

        res = {}
        for op in ops:
            rels = []
            page = 1
            while True:
                tmp = self.do_get("/urls/relationships/x-operations/" + op['_id'] + f"?page={page}&max_results=25")["_items"]
                if not tmp:
                    break
                rels += tmp
                page += 1
            res[op["name"]] = []
            for rel in rels:
                res[op["name"]].append(rel['value'])
        return res

    def CTIS_login(self, user, password):
        #response = requests.post(f"{self.url}/api/auth/login", json={"username": user, "password": password})
        response = requests.get(f"{self.url}/login", auth=(user, password))
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + response.json()["data"]["access_token"]}
