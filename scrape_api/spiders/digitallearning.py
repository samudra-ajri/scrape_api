# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.utils.project import get_project_settings
from scrapy.selector import Selector
from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import datetime


class DigitallearningSpider(scrapy.Spider):
    global auth, CLEANR
    settings = get_project_settings()

    auth = settings.get('DIGITALLEARNING_SESSION')
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\r\n')
    
    name = 'digitallearning'
    allowed_domains = ['digitallearning.telkom.co.id']

    def start_requests(self):
        yield scrapy.Request(
            url='https://digitallearning.telkom.co.id/enrol/index.php?id=1',
            callback=self.parse,
            cookies={
                'MoodleSession': auth,
            }
        )

    def parse(self, response):
        for i in range(5001):
            yield scrapy.Request(
                url=f'https://digitallearning.telkom.co.id/enrol/index.php?id={100 + i}',
                callback=self.parse_2,
                cookies={
                    'MoodleSession': auth,
                }
            )

    def parse_2(self, response):
        CLEANIMG = re.compile('\(([^)]+)\)')

        title = response.xpath("//title/text()").get()
        description = response.xpath("//title/text()").get()
        img_raw = response.xpath("//div[@class='imgbox']").get()
        if img_raw and CLEANIMG.search(img_raw):
            img_url = re.search(r'\((.*?)\)',img_raw).group(1)
        else:
            img_url = None

        yield {
            'title': title.strip() if title else response.request.url,
            'description': re.sub(CLEANR, '', description.strip()) if description else title,
            'url': response.request.url.replace('course/view', 'enrol/index'),
            'img_url': img_url,
            'content_type': 'digitallearning',
            'published_date': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'elastic': 0,
            'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }