# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TanzaniaGazetteItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    # name = scrapy.Field()
    pass
