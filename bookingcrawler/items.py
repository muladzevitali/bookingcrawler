# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookingcrawlerItem(scrapy.Item):
    date = scrapy.Field()
    author = scrapy.Field()
    country = scrapy.Field()
    number_of_avaliations = scrapy.Field()
    score = scrapy.Field()
    title = scrapy.Field()
    positive = scrapy.Field()
    negative = scrapy.Field()
