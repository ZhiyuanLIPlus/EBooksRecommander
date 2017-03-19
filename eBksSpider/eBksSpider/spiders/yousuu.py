# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from eBksSpider.items import eBookItem,eBookListItem
import logging

class YousuuSpider(scrapy.Spider):
    name = "yousuu"
    allowed_domains = ["yousuu.com"]
    start_urls = ['http://www.yousuu.com/booklist']
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Referer": "http://www.yousuu.com/"
    }

    def start_requests(self):
        logging.info("Prepare logging...")
        #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        #登陆成功后, 会调用after_login回调函数
        return [FormRequest(url="http://www.yousuu.com/login",
                            method= "POST",
                            #meta = {'cookiejar' : response.meta['cookiejar']},
                            headers = self.headers,  #注意此处的headers
                            formdata = {
                            'username': '371053515@qq.com',
                            'password': 'fzyl890705'
                            },
                            callback = self.after_login,
                            dont_filter = True
                            )]
        #return [Request("http://www.yousuu.com/login", meta = {'cookiejar' : 1}, callback = self.post_login)]

    def post_login(self, response):
        logging.info("Prepare logging...")
        #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        return [FormRequest.from_response(response, method= "POST",
                            meta = {'cookiejar' : response.meta['cookiejar']},
                            headers = self.headers,  #注意此处的headers
                            formdata = {
                            'username': '371053515@qq.com',
                            'password': 'fzyl890705'
                            },
                            callback = self.after_login,
                            dont_filter = True
                            )]

    def after_login(self, response) :
        for url in self.start_urls:
            yield self.make_requests_from_url(url, callback = self.parse)

    def parse(self, response):

        pass
