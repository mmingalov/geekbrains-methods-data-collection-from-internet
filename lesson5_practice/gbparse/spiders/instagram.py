# -*- coding: utf-8 -*-
import re
import json
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
import scrapy
from urllib.parse import urlencode
from lesson5_practice.gbparse.items import InstaItem

HASHES = {
    'followers': 'c76146de99bb02f6415203be841dd25a',
    'following': 'd04b0a864b4b54837c0d870b0e77e076',
    'media': '58b6785bea111c67129decbe6a448951',
    'media_comments': '97b41c52301f77ce508f55e66d17620e',
    'likes': 'd5d763b1e2acf209d62d22d184488e57',
    'tags': '174a5243287c5f3a7de741089750ab3b',

}

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'gb_scarto'
    inst_pass = 'scartohorse123'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = 'vol3397'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    user_data_hash = 'c9100bf9110dd6361671f113dd02e7d6'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'password': self.inst_pass},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.userdata_parse,
                cb_kwargs={'username': self.parse_user}
            )

    def userdata_parse(self, response: HtmlResponse, username):
        #нам нужно собрать запрос к API
        user_id = self.fetch_user_id(response.text, username)
        varibles = {
            'user_id': user_id,
            "include_chaining": True,
            "include_reel": True,
            "include_logged_out_extras": False,
        }
        url = f'{self.graphql_url}query_hash={self.user_data_hash}&{urlencode(varibles)}' #urlencode кодирует наш словарик для корректной передачи в параметры запроса
        #получили ссылку для запроса к API
        yield response.follow(
            url,
            callback=self.user_data,
            cb_kwargs={'username': username}
        )


    def user_data(self, response: HtmlResponse, username):
        j_user_data = json.loads(response.text)

        item = ItemLoader(InstaItem(), response)
        # item.add_value('url', response.url)
        item.add_value('dict', j_user_data)
        item.add_value('url', response.url)
        item.add_value('user_id', response.user_id)

        yield item.load_item()

        print(1)

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
