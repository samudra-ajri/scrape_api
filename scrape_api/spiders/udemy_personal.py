# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.utils.project import get_project_settings
from scrapy.selector import Selector
from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import datetime


class UdemyPersonalSpider(scrapy.Spider):
    name = 'udemy_personal'
    allowed_domains = ['digilearn.udemy.com']

    def start_requests(self):
        yield scrapy.Request(
            url='https://digilearn.udemy.com/api-2.0/discovery-units/all_courses/?page_size=50&category_id=320&source_page=org_category_page&sos=pc&fl=cat&p=1',
            callback=self.parse,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
            }
        )

    def parse(self, response):
        resp = json.loads(response.body)
        items = resp.get('unit').get('items')
        for item in items:
            yield {
                'title': item.get('title'),
                'description': item.get('headline'),
                'url': f'https://digilearn.udemy.com{item.get("url")}',
                'img_url': item.get('image_480x270'),
                'content_type': 'digilearnudemy',
                'published_date': item.get('published_time'),
                'elastic': 0,
                'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            }

        if len(items) != 0:
            parsed_url = urlparse(response.request.url)
            next_page = int(parse_qs(parsed_url.query)['p'][0]) + 1

            yield scrapy.Request(
                url=f'https://digilearn.udemy.com/api-2.0/discovery-units/all_courses/?page_size=16&category_id=320&source_page=org_category_page&sos=pc&fl=cat&p={next_page}',
                callback=self.parse,
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
                }
            )