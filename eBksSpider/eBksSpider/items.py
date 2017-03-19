# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class eBookItem(scrapy.Item):
    id = Field()
    name = Field()
    author = Field()
    noteInBooklist = Field()
    noteGeneral = Field()
    status = Field()
    wordCount = Field()
    numOfComments = Field()

class eBookListItem(scrapy.Item):
    name = Field()
    publisher = Field()
    publisher_url = Field()
    type = Field()
    numOfLike = Field()
    bookList = Field()
    url = Field()

class EbksspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Website(Item):
    name = Field()
    description = Field()
    url = Field()