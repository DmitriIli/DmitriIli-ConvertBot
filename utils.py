from config import url
import requests
import json


class InputError(Exception):
    pass


class API_request:

    @staticmethod
    def get_price():
        r = requests.get(url)
        json_dict = json.loads(r.content)

        values = {
            'USD': float(json_dict['rates']['USD']),
            'RUB': float(json_dict['rates']['RUB']),
            'EUR': 1
        }
        return values
