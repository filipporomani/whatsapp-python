import requests


def authorized(self) -> bool:
    return requests.get(self.url, headers=self.headers).status_code != 401
