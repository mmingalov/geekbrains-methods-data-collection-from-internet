# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import scrapy
# from scrapy.pipelines.images import ImagesPipeline

mongo_client = MongoClient()

class VKPipeline(object):
    def process_item(self, item, spider):
        database = mongo_client[spider.name]
        collection = database[type(item).__name__]
        collection.insert_one(item)
        print(f'Item was inserted.')
        return item