# Рессурс к парсингу : https://5ka.ru/
# Задача:
# Необходимо собрать все данные с раздела товаров по акции и сохранить в json файлы: где имя файла это имя категории товара.
#
# Структура данных в виде:
#
# {
# category_id: str,  - уникальный идентификатор категории
# category_name: str, - человекочитаемое имя категории
# items: list - список товаров пренадлежищий к данной категории
# }
import requests
import time
import json

def get_data(url: str, params: dict) -> dict:
    while True:
        time.sleep(1)
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            print('200')
            break
    return response.json()

#STARTING
headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko)',
}
params = {'records_per_page': 100, 'page': 1}

url = 'https://5ka.ru/api/v2/special_offers/'
results = []

while url:
    response = get_data(url, params)
    results.extend(response['results'])
    url = response['next']
    params = {}
print(1)

#ПРМЕЧАНИЕ: сайт не открываеся, ссылка 'https://5ka.ru/api/v2/special_offers/' возвращает пусто
#включаем полную импровизацию. КОД будет отдаленно напоминать следующее:

# for item in results: #у нас есть список товаров по акции
#     dict = {'category_id': item['category_id'], category_name
