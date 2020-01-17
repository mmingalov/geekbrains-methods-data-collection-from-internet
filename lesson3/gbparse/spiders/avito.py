# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/habarovsk/kvartiry/prodam?cd=1']
        #https://www.avito.ru/habarovsk/kvartiry/prodam?cd=1&p=2

    def parse(self, response: HtmlResponse):
            #next_page = response.css('ul.gb__pagination li.page a[rel=next]::attr(href)').extract_first()
        next_page = response.css('div.pagination-root-2oCjZ li.page a[rel=next]::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        posts = response.css('div.post-items-wrapper div.post-item a.post-item__title::attr(href)').extract()
        for post in posts:
            yield response.follow(post, callback=self.post_parse)

    def post_parse(self, response: HtmlResponse):
        title = response.css('article h1::text').extract_first()
        date = response.css('article time::attr(datetime)').extract_first()

        yield {
            'title': title,
            'date': date,
        }
