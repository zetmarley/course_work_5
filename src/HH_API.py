import requests
import json

class HH_API():
    """Параметры"""
    url = 'https://api.hh.ru/employers'
    response = requests.get(url)
    page = json.loads(response.text)

    def __init__(self):
        pass