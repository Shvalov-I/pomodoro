import requests
from datetime import datetime
import threading
import os

USERNAME = os.getenv("PIXELA_USERNAME")
TOKEN = os.getenv("PIXELA_TOKEN")

PIXEL_ENDPOINT = f"https://pixe.la/v1/users/{USERNAME}/graphs/graph1"

HEADERS = {
    "X-USER-TOKEN": TOKEN,
}


class ProgrammingGraph:
    def __init__(self):
        self.today = datetime.now()
        self.today = self.today.strftime("%Y%m%d")
        self.today_score = 0.0

    def get_today_score(self):
        try:
            response = requests.get(url=f"{PIXEL_ENDPOINT}/{self.today}", headers=HEADERS)
            today_score = float(response.json()["quantity"])
        except KeyError:
            self.today_score = 0.0
            #print("not Get today score")
        else:
            self.today_score = today_score
            #print("Get today score")

    def update_score(self, score: float):
        self.get_today_score()
        new_score = score + self.today_score
        new_score_params = {
            "date": self.today,
            "quantity": f"{round(new_score, 2)}",
        }
        response = requests.post(url=PIXEL_ENDPOINT, json=new_score_params, headers=HEADERS)
        #print(response.json())

    def calculate_score(self, current_score: float):
        t = threading.Thread(target=self.update_score, args=(current_score,))
        t.start()





