import requests


class CTIS():

    headers = {}
    url = ""

    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.CTIS_login(username, password)

    def do_req(self, url):
        return requests.get(self.url + url, headers=self.headers).json()

    # Horrible, to enhance
    def get_operations_and_urls(self, op_label):
        # TODO: add where _created gte today minus a configurable interval
        ops = self.do_req(
            f"/x-operations?where=%7B%22labels%22%3A%20%5B%22{op_label}%22%5D%7D")["_items"]
        res = {}
        for op in ops:
            rels = self.do_req("/urls/relationships/x-operations/"+op['_id'])
            res[op["name"]] = []
            for rel in rels['_items']:
                res[op["name"]].append(rel['value'])
        return res

    def CTIS_login(self, user, password):
        #response = requests.post(f"{self.url}/api/auth/login", json={"username": user, "password": password})
        response = requests.get(f"{self.url}/login", auth=(user, password))
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + response.json()["data"]["access_token"]}
