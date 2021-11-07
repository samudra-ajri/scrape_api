# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.utils.project import get_project_settings
from datetime import datetime


class DigilearnArticleSpider(scrapy.Spider):
    global auth, CLEANR
    settings = get_project_settings()

    name = 'digilearn_article'
    allowed_domains = ['service.mydigilearn.id']

    auth = settings.get('DIGILEARN_AUTH_HEADER')
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\r\n')

    def start_requests(self):
        yield scrapy.Request(
            url='https://service.mydigilearn.id/v2/articles/list?perpage=50&page=1',
            callback=self.parse,
            headers={
                'Authorization': auth
            }
        )

    def parse(self, response):
        resp = json.loads(response.body)
        items = resp.get('data').get('results')
        sites = []
        for item in items:
            url = f'https://service.mydigilearn.id/v2/articles/{item.get("id")}'
            sites.append(url)
        
        for site in sites:
            yield scrapy.Request(
                url=site,
                callback=self.parse_2,
                headers={
                    'Authorization': auth
                }
            )

        next_page = resp.get('data').get('pagination').get('next')
        total_pages = resp.get('data').get('pagination').get('total_pages')
        if next_page <= total_pages:
            yield scrapy.Request(
                url=f'https://service.mydigilearn.id/v2/articles/list?perpage=50&page={next_page}',
                callback=self.parse,
                headers={
                    'Authorization': auth
                }
            )

    def parse_2(self, response):
        resp = json.loads(response.body)
        item = resp.get('data')
        yield {
            'title': item.get('title'),
            'description': re.sub(CLEANR, '', item.get('content')) if item.get('content') else item.get('title'),
            'url': f'https://www.mydigilearn.id/article/{item.get("id")}/{item.get("slug")}',
            'img_url': item.get('picture'),
            'content_type': 'digilearn',
            'published_date': item.get('created_at') if item.get('created_at') else datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'elastic': 0
        }