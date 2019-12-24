import requests
import time

headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko)',
}
params = {'records_per_page': 100, 'page': 1}

api_url_category = 'https://5ka.ru/api/v2/categories/'
api_url = 'https://5ka.ru/api/v2/special_offers/'


# url = 'https://5ka.ru/special_offers/'


class CategoryObj:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def get_data(url: str, params: dict) -> dict:
    while True:
        time.sleep(1)
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            break
    return response.json()


url = 'https://5ka.ru/api/v2/special_offers/'
results = []

while url:
    response = get_data(url, params)
    results.extend(response['results'])
    url = response['next']
    params = {}
print(1)
