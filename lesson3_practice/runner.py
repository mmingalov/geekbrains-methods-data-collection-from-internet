from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson3_practice.avitoparse import settings
from lesson3_practice.avitoparse.spiders.avito import AvitoSpider #паук для Урок 3

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    # process.crawl(GeekbrainsSpider) #задаем паука из Урок 3
    process.crawl(AvitoSpider)  # задаем паука из ДЗ к Урок 3
    process.start()


# Ресурс: avito.ru/
#
# Раздел: недвижимость квартиры продать
# Ваша задача обойти все объявления, извлечь следующие данные:
    # Заголовок
    # цена
    # Список параметров объекта
# Все полученные данные сохранить в коллекцию MongoDB
# Парсинг осуществлять с помощью scrapy