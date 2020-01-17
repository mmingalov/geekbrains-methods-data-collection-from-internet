# ЗАДАНИЕ:
# используя bs4
# рессурс: https://geekbrains.ru/posts
#
# todo пройти ленту статей блога, получить страницу со статьей,
# todo зайти на страницу и
# todo извлечь следующие данные: заголовок статьи, дата публикации, url, список тегов, имя автора, url автора
# todo при помощи sqlalchemy сохранить данные в базу.
# обязательно теги и автор должны существовать отдельными таблицами, и должны быть корректно реализованы соответсвующие связи.

import requests
from bs4 import BeautifulSoup

def get_link_next_page(page_num):
    if page_num == 1:
        link = "https://geekbrains.ru/posts"
    else:
        link = "https://geekbrains.ru/posts" + '?page=' + str(page_num)
    return link

def define_pagination_last_page():
    url = "https://geekbrains.ru/posts"
    response = requests.get(url)
    soap = BeautifulSoup(response.text, 'lxml')
    ul = soap.find_all('ul', attrs={'class':'gb__pagination'})
    result = ul[0].contents[4].string
    return int(result)

N = define_pagination_last_page()
list=[]
for p in range(1,N+1):
    current_page = get_link_next_page(p)
    response = requests.get(current_page)
    soap = BeautifulSoup(response.text, 'lxml')
    print('Текущая страница:', current_page)
    topics = soap.find('div', attrs={'class':'post-items-wrapper'}).find_all('a', attrs={'class':'post-item__title h3 search_text'})
    for n in topics:
        # dict = {}
        link = n.get("href")
        # print(link)
        post_link = 'https://geekbrains.ru'+link
        print(post_link)
        response2 = requests.get(post_link)
        soap2 = BeautifulSoup(response2.text, 'lxml')

        # заголовок статьи, дата публикации, url, список тегов, имя автора, url автора
        title_post = soap2.find('h1').string
        # print('title_post',title_post)
        date_post = soap2.find('div', attrs={'class':'blogpost-date-views'}).find('time', attrs={'class':'text-md text-muted m-r-md'}).string
        url_post = post_link
        # tags_post = soap2.find('i',attrs={'class':'i i-tag m-r-xs text-muted text-xs'})['keywords']
        tags_post = soap2.find_all('a', attrs={'class': 'small'})
        author_name = soap2.find('div',attrs={'class':'col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v'}).find('a').find('div',attrs={'class':'text-lg text-dark'}).string
        author_url = 'https://geekbrains.ru'+ soap2.find('div',attrs={'class':'col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v'}).find('a')['href']

        li = []
        for m in tags_post:
            l = m.get("href")
            li.append(l.replace("/posts?tag=",""))
        #поместим собранную информацию с словарь dict
        dict = {
            'title_post':title_post,
            'date_post':date_post,
            'url_post':url_post,
            'tags_post':li,#tags_post,
            'author_name':author_name,
            'author_url':author_url
        }
        print(dict)

        #соберем все словари (посты) в единый список постов
        list.append(dict)
print(list) #список всех тэгов (словарей)

from sqlalchemy.orm import relationship


