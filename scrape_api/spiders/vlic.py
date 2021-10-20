# -*- coding: utf-8 -*-
import scrapy


class VlicSpider(scrapy.Spider):
    name = 'vlic'
    allowed_domains = ['youtube.googleapis.com']
    start_urls = ['http://youtube.googleapis.com/']

    def parse(self, response):
        pass
