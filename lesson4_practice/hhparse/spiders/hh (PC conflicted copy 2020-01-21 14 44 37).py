# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import HtmlResponse
from lesson4_practice.hhparse.items import hhparseItem

# https://vladivostok.hh.ru/search/vacancy?L_is_autosearch=false&area=22&clusters=true&enable_snippets=true&text=%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82%D0%BE%D0%BB%D0%BE%D0%B3&page=0
class HhSpider(scrapy.Spider):
    name = 'headhunter'
    allowed_domains = ['hh.ru']
    start_urls = [f'https://vladivostok.hh.ru/search/vacancy?L_is_autosearch=false&area=22&clusters=true&enable_snippets=true&text=%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82%D0%BE%D0%BB%D0%BE%D0%B3&page={idx}' for idx in range (0,4)]

    def parse(self, response: HtmlResponse):
        print(1)
        #// в одном из детей
        # urls = response.xpath('//div[contains(@data-maker,"item")]/div[@class="item__line"]//h3/a[@itemprop="url"] ')
        urls = response.xpath('//div[@class="resume-search-item__name"]//a/@href').extract()
        for url in urls:
            yield response.follow(url, callback=self.post_parse)

    def post_parse(self, response: HtmlResponse):
        pattern = re.compile('[0123456789]')
        # item = hhparseItem(
        url=response.url
        title= response.xpath('//h1/span/text()').extract_first() # title=response.xpath('//h1[@class="header"]/span/text()').extract_first,

        # salary=int(response.xpath('//div[@class="vacancy-title"]/p[@class="vacancy-salary"]/text()').extract()[1].replace('\xa0','')),
        salary = ''.join(response.xpath('//div[@class="vacancy-title"]/p[@class="vacancy-salary"]/text()').extract()).replace('\xa0',''),

        skills=response.xpath('//div[@class="vacancy-description"]//div[@class="vacancy-section"]//span[@data-qa="bloko-tag__text"]/text()').extract()
        company_name=response.xpath('//div[@class="vacancy-company-wrapper"]/div[@data-qa="vacancy-company"]//a[@itemprop="hiringOrganization"]/span[@itemprop="name"]/span/text()').extract_first()
        company_link=response.xpath('//div[@class="vacancy-company-wrapper"]/div[@data-qa="vacancy-company"]//a[@itemprop="hiringOrganization"]/@href').extract()
        pass
        # )

# Заголовок
# URL
# Предлагаемая ЗП
# Список ключевых навыков
# Название организации разместившей вакансию
# Ссылка на страницу организации разместившей организацию