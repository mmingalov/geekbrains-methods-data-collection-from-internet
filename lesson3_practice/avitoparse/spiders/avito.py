# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/habarovsk/kvartiry/prodam?cd=1'] #первая страница, с которой что-то парсим

    def parse(self, response: HtmlResponse):
        next_page = response.css('div.pagination-hidden-3jtv4 a.pagination-page::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        # posts = response.css('div.post-items-wrapper div.post-item a.post-item__title::attr(href)').extract()

        #объявления
        posts = response.css('div.js-catalog_serp div.snippet-horizontal a.snippet-link::attr(href)').extract()
        for post in posts:
            yield response.follow(post, callback=self.post_parse)

    def post_parse(self, response: HtmlResponse):
        # title = response.css('div.title-info-main h1.title-info-title').extract_first()
        title = response.css('div.title-info-main span.title-info-title-text::text').extract_first()
        price = response.css('div.item-price-value-wrapper span.js-item-price::attr(content)').extract_first()

        list = response.css('ul.item-params-list li.item-params-list-item').extract()
        list2 = response.css('ul.item-params-list span.item-params-label::text').extract()
        list3 = response.css('ul.item-params-list li.item-params-list-item::text').extract()

        for i,item in enumerate(list3[:]):
            if item==' ':
                list3.remove(item)
        dict = {}
        for i,item in enumerate(list2):
            dict[item] = list3[i]

#        param_name = 1

        yield {
            'title': title,
            'price': price,
            'list':dict #list,
        }
