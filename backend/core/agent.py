from setup.settings import API_HOST, API_PORT
from typing import Dict
import requests

class Agent(object):
    def __init__(self):
        self.url = f"http://{API_HOST}:{API_PORT}"

    def get_news(self) -> Dict[str, str]:
        try:
            response = requests.get(
                url=f"{self.url}/generate-news",
                headers={'content-type': 'application/json'}
            )
            if response.status_code in [200, 201, 204]:
                return response.json()
            else:
                raise Exception("Error to get news!")
        except Exception as e:
            raise (e)