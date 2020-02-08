from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from course_work.gbparse import settings
# from course_work.gbparse.spiders.instagram import InstagramSpider
from course_work.gbparse.spiders.vk import VKSpider

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    process.crawl(VKSpider)
    process.start()

#