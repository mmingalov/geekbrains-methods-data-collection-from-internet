from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gbparse import settings
from lesson5.gbparse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    # process.crawl(GeekbrainsSpider)
    process.crawl(InstagramSpider)
    process.start()
