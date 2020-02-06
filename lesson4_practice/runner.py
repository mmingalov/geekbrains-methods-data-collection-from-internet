from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson4_practice.hhparse import settings
from lesson4_practice.hhparse.spiders.hh import HhSpider #паук для Урок 4

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    process.crawl(HhSpider)  # задаем паука из ДЗ к Урок 4
    process.start()


# Ресурс: HH.ru
# Регион не важен,
# Ваша задача перейти список любой из вакансий пройти этот список, пройти пагинацию зайди на страницу с вакансией и извлечь следующие данные
#
# Заголовок
# URL
# Предлагаемая ЗП
# Список ключевых навыков
# Название организации разместившей вакансию
# Ссылка на страницу организации разместившей организацию
# Ссылку на логотип организации