# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
import re
from eBksSpider.items import eBookItem,eBookListItem

import logging

class YsxpathtestSpider(scrapy.Spider):
    name = "ysXpathTest"
    allowed_domains = ["yousuu.com"]
    start_urls = ['http://www.yousuu.com/booklist']
    MAXPAGE = 50000
    begin = 0

    def parse(self, response):
        items = []
        for tr in response.xpath('//tr'):
            newBookList = eBookListItem()
            #Nb of Likes
            votes = tr.xpath('.//td/a[contains(@class, "votes")]/small/text()').extract_first()
            newBookList['numOfLike'] = votes #[0] if votes is not None else 0
            #Type
            types = tr.xpath('.//td/h4/small/text()').extract_first()
            #print types
            newBookList['type'] = types #[0].strip('[').strip(']') if types is not None else ""
            #Name
            names = tr.xpath('.//td/h4/a/text()').extract_first()
            #print names
            newBookList['name'] = names  #[0] if names is not None else ""
            #URL
            urls = tr.xpath('.//td/h4/a/@href').extract_first()
            url = response.urljoin(urls)
            newBookList['url'] = url #[0] if urls is not None else ""
            #Publisher
            publishers = tr.xpath('.//td/p/a[contains(@href, "user")]/text()').extract_first()
            newBookList['publisher'] = publishers
            #Publisher_url
            publishers_url = tr.xpath('.//td/p/a[contains(@href, "user")]/@href').extract_first()
            newBookList['publisher_url'] = response.urljoin(publishers_url)
            #print newBookList['publisher_url']
            #print newBookList['name']
            newBookList['bookList'] = []
            yield scrapy.Request(url, meta={'item': newBookList}, callback=self.parse_booklist)
            #items.append(newBookList)
        href = response.xpath('//a[contains(@onclick, "jumpurl")]/@onclick').extract()

        #Get next page
        #if we get the same page struct
        if len(href) >= 3:
            split_url = href[1].split('\'')
            logging.info( "******************* NEXT Page:" + self.start_urls[0] + "?" + split_url[1] + "=" + split_url[3])
            nextPage_url = self.start_urls[0] + "?" + split_url[1] + "=" + split_url[3]
            if self.begin <= self.MAXPAGE :
                self.begin += 1
                logging.info("******************* Count:" + str(self.begin))
                yield scrapy.Request(nextPage_url, callback=self.parse)

        #return items
    def parse_booklist(self,response):
        newBookList = response.meta['item']
        bookListToAdd = newBookList['bookList']
        #bookListToAdd = [] if newBookList['bookList'] is None else newBookList['bookList']
        for booklistItem in response.xpath('//div[contains(@class, "booklist-item")]/div/div[contains(@class, "booklist-subject")]'):
            #newBook = eBookItem()
            newBook = {}
            #Id
            shortUrl = booklistItem.xpath('.//div[@class="title"]/a[contains(@href, "book")]/@href').extract_first()
            newBook['id'] = shortUrl.split('/')[-1] if shortUrl is not None else -100
            #Name
            names = booklistItem.xpath('.//div[@class="title"]/a[contains(@href, "book")]/text()').extract_first()
            newBook['name'] = names
            #author
            authors = booklistItem.xpath('.//div[@class="abstract"]/text()').extract_first()
            newBook['author'] = authors.split(':')[-1]
            #noteInBooklist
            stars = booklistItem.xpath('.//div[@class="abstract"]/span[@class="num2star"]/text()').extract_first()
            if stars is None:
                continue
            newBook['noteInBooklist'] = int(stars)
            #noteGeneral
            noteGeneralToStrip = booklistItem.xpath('.//div[@class="meta"]/span[@class="source"]/text()').extract_first()
            newBook['noteGeneral'] = [float(s) for s in re.findall(r'\d+\.\d+', noteGeneralToStrip)][0]
            #status
            #wordCount
            #numOfComments
            spanArray = booklistItem.xpath('.//div[@class="rating"]/span/text()').extract()
            numOfCommentsToStrip = spanArray[0]
            newBook['numOfComments'] = [int(s) for s in re.findall(r'\b\d+\b', numOfCommentsToStrip)][0]
            #print newBook
            bookListToAdd.append(newBook)
        newBookList['bookList'] = bookListToAdd
        liPage = response.xpath('//div[@class="ro"]/ul/li')
        if len(liPage) > 0:
            nPage = len(liPage)
            nPage /= 2
            nPage -= 2
            for indexPage in range(2, nPage + 1):
                subPageURL = newBookList['url']+"?page="+str(indexPage)
                yield scrapy.Request(subPageURL, meta={'item': newBookList}, callback=self.parse_booklist)
        else:
            yield newBookList

