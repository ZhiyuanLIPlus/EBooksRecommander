# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
tempDictParse = {}
class EbksspiderPipeline(object):
    def __init__(self):
        #self.file = open('test.json', 'wb')
        self.file = codecs.open('test.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        '''

        :param item:
        :param spider:
        :return:
        '''
        tempDictParse['name'] = item['name']
        tempDictParse['publisher'] = item['publisher']
        tempDictParse['publisher_url'] = item['publisher_url']
        tempDictParse['type'] = item['type']
        tempDictParse['numOfLike'] = item['numOfLike']
        tempDictParse['bookList'] = item['bookList']
        tempDictParse['url'] = item['url']

        line = json.dumps(tempDictParse) + "\n"
        self.file.write(line.decode('unicode_escape'))
        return item

    def spider_closed(self, spider):
        self.file.close()
