# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.utils.project import get_project_settings
from scrapy.selector import Selector
from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import datetime

class LabatrSpider(scrapy.Spider):
    global CLEANR

    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\r\n')

    name = 'labatr'
    allowed_domains = ['labatr.id']

    start_urls = [f'https://labatr.id/']

    def parse(self, response):
        items = response.xpath("//div[@class='card']")
        for item in items:
            yield {
                'title': item.xpath(".//h4[@class='card-title']/text()").get(),
                'description': item.xpath(".//p[@class='card-text']/text()").get(),
                'url': item.xpath(".//a/@href").get(),
                'img_url': item.xpath(".//img/@src").get(),
                'content_type': 'labatr',
                'published_date': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                'elastic': 0,
                'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            }        