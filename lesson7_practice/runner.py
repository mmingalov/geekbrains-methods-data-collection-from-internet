from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson7_practice.gbparse import settings
# from lesson5_practice.gbparse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    process.crawl(InstagramSpider)
    process.start()

# ресурс:
# Необходимо найти заводские серийные номера кассовых аппаратов из изображений и страниц PDF файлов.
# В конечном результате должна полуичться MongoDb база данных в которой явно и наглядно понятно из какого изначального файла был добыт номер или несколько номеров.
# Так же должна быть коллекция в БД в которой указаны пути к файлам из которых не удалось извлечь номера с указанием страницы если изначально это PDF документ.
