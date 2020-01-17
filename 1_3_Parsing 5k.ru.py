# _3. Рессурс к парсингу : https://5ka.ru/
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

def main_parser():
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
    return results


def save_data_json(name,results):
    with open (name,'w') as f:
        json_results=json.dump(results,f)

def open_data_json():
    with open ('1_3_special_offers.json','r') as f:
        results = json.load(f)
        return results

#MAIN
# results = main_parser()

# save_data_json('1_3_special_offers.json',results) #ПРИМЕЧАНИЕ: сайт часто не открываеся, ссылка 'https://5ka.ru/api/v2/special_offers/' возвращает пусто. Поэтому для отладки сохраним результат в файл
with open('1_3_special_offers.json', 'r') as f:
    results = json.load(f)

set_categ = set() #определили множество категорий товаров
for d in results:
    categ = d['promo']['description']
    set_categ.add(categ)
    # print(categ)

list_categ = [] #определили список резульирующих словарей. Его размер совпадает с размером множества set_categ
for s in set_categ:
    dict = {'category_id':None, 'category_name':s, 'items':[]}
    for d in results:
        categ_name = d['promo']['description']
        categ_id = d['promo']['id']
        item_name = d['name']
        if categ_name == s:
            dict['category_id'] =categ_id
            dict['items'].append(item_name)
    list_categ.append(dict) #добавляем словарь со всеми товарами катгории s
    save_data_json(s + '.json',dict)
print(set_categ)