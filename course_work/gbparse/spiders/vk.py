# -*- coding: utf-8 -*-
import json
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
import scrapy
from urllib.parse import urlencode
from course_work.gbparse.items import GraphItem
import vk

# url = 'https://api.vk.com/method/friends.get?v=5.52&access_token=' + access_token
#     url = url + '&user_id=' + str(user)

class VKSpider(scrapy.Spider):
    # ID приложения   7308366
    # Защищенный ключ aprF938fcdB8R9KrhoLo
    # Сервисный ключ доступа  134464c3134464c3134464c351132be08d11344134464c34d7e56ba71e7144c295bab1c
    access_token = '913cbd317b158a61a30b4844eadab0671b7cf5e55fa6331e0745edd44e45f8cfc0780d9044983e6bd25e5'
    service_access_key = '134464c3134464c3134464c351132be08d11344134464c34d7e56ba71e7144c295bab1c'

    name = 'vk'
    allowed_domains = ['vk.com']


    USER1 = 'https://vk.com/id6244012'
    USER2 = 'https://vk.com/id30870147'  #Екатерина Дорожкина связь прямая
    # USER2 = 'https://vk.com/id7704548' #Александра Бегун, через 1-го -- три разных графа
    # USER2 = 'https://vk.com/id9787523' #Евгения Леонтьева, через 1-го -- три разных графа, через 2-их три разных графа

    user1_id = int(USER1.replace('https://vk.com/id', '').replace('https://vk.com/', ''))
    user2_id = int(USER2.replace('https://vk.com/id', '').replace('https://vk.com/', ''))

    #настраиваемся на VK.api
    session = vk.Session(access_token=access_token)
    vk_api = vk.API(session)
    start_urls = [USER1]
    response1 = vk_api.friends.get(user_id=user1_id,v="5.8")
    user1_friends = response1["items"]

    user1_friends = [30870147,4921405,6182129,278075880] # тимофеев [гегельская, берсенев, рыжова] - Уровень 0 и 1
    # user1_friends = [560056, 803898]  # [зейбель, тимшин] - Уровень 2
    # user1_friends = [560056]

    graph = [None] * 10
    graph[0] = user1_id
    # друзья первого уровня
    def parse(self, response: HtmlResponse):
        for user in self.user1_friends:
            self.graph[1] = user
            print(f'PARSE: ({user}, {self.get_username(user)}) user of first level. Number of Friends: {len(self.user1_friends)}')
            if user == self.user2_id:
                print('PARSE: Граф найден на первом уровне')
                print(self.graph)
                graph_ = list(filter(lambda x: x != None, self.graph))
                graph_names_ = list(map(lambda x: self.get_username(x), graph_))
                item = GraphItem(
                    user1={
                        "link": self.USER1,
                        "id": self.user1_id,
                        "username": self.get_username(self.user1_id)
                    },
                    user2={
                        "link": self.USER2,
                        "id": self.user2_id,
                        "username": self.get_username(self.user2_id)
                    },
                    graph_id=tuple(graph_),
                    graph_username=graph_names_,
                )
                yield item
                self.close(VKSpider,"Graph found")

            user_path = 'https://vk.com/id'+ str(user)
            yield response.follow(user_path,
                                  callback=self.f_parse,
                                  cb_kwargs={'user_id': user,
                                             'level':1}
                                  )

    # друзья последующих уровней
    def f_parse(self, response: HtmlResponse, user_id: str, level: int):
        try:
            resp = self.vk_api.friends.get(user_id=user_id, v="5.8")
        except vk.exceptions.VkAPIError as e:
            print(f'User {user_id} {self.vk_api.users.get(user_id=user_id, v="5.8")} -- {e.message}')
            #vk.exceptions.VkAPIError: 15. Access denied: this profile is private
            #vk.exceptions.VkAPIError: 18. User was deleted or banned
            return None
        f_level = level + 1

        user_friends = resp["items"]
        try:
            user_friends.remove(self.user1_id)
        except:
            pass

        print(f'PARENT_USER:{user_id} ({self.get_username(user_id)}), level:{level} ,friends:{len(user_friends)}')
        for idx, f in enumerate(user_friends):
            # self.graph[f_level] = f
            self.graph[level]=user_id
            if f==self.user2_id:
                self.graph[f_level] = f
                print(f'F_PARSE(user:{user_id}): graph has been found on level:{f_level} user(idx:{idx}, {f}, {self.get_username(f)})!')
                print(self.graph)
                graph_ = list(filter(lambda x: x != None, self.graph))
                graph_names_ = list(map(lambda x: self.get_username(x), graph_))
                item = GraphItem(
                    user1={
                        "link": self.USER1,
                        "id": self.user1_id,
                        "username": self.get_username(self.user1_id)
                    },
                    user2={
                        "link": self.USER2,
                        "id": self.user2_id,
                        "username": self.get_username(self.user2_id)
                    },
                    graph_id=tuple(graph_),
                    graph_username=graph_names_,
                )
                yield item
                self.close(VKSpider, "Graph found")

            f_path = 'https://vk.com/id'+ str(f)
            yield response.follow(
                f_path,   #self.parse_user
                callback=self.f_parse,
                cb_kwargs={'user_id': f,
                           'level': f_level} #self.parse_user
            )
        print(f"Пройдены все друзья ({idx}) пользователя {user_id} ({self.get_username(user_id)})")

    def get_username(self, user: int):
        username = None
        try:
            info = self.vk_api.users.get(user_id=user, v="5.8")

            first_name = info[0]["first_name"]
            last_name = info[0]["last_name"]
            username = first_name + ' ' + last_name
        except:
            pass
        return username

# def get_username2(self, api: vk.API, user: int):
#     try:
#         info = api.users.get(user_id=user, v="5.8")
#
#         first_name = info[0]["first_name"]
#         last_name = info[0]["last_name"]
#         username = first_name + ' ' + last_name
#     except:
#         username = None
#     return username