# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.utils.project import get_project_settings
from datetime import datetime


class DigilearnPathwaySpider(scrapy.Spider):
    global auth, CLEANR
    settings = get_project_settings()

    name = 'digilearn_pathway'
    allowed_domains = ['service.mydigilearn.id']

    auth = settings.get('DIGILEARN_AUTH_HEADER')
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\r\n')

    def start_requests(self):
        yield scrapy.Request(
            url='https://service.mydigilearn.id/pathway/list?limit=50&page=1',
            callback=self.parse,
            headers={
                'Authorization': auth
            }
        )

    def parse(self, response):
        resp = json.loads(response.body)
        items = resp.get('result').get('datas')
        sites = []
        for item in items:
            url = f'https://service.mydigilearn.id/pathway/{item.get("id")}'
            sites.append(url)
        
        for site in sites:
            yield scrapy.Request(
                url=site,
                callback=self.parse_2,
                headers={
                    'Authorization': auth
                }
            )

        current_page = resp.get('result').get('pagination').get('page')
        next_page = current_page + 1
        total_items = resp.get('result').get('pagination').get('totalItems')
        limit = resp.get('result').get('pagination').get('limit')
        if current_page*limit <= total_items:
            yield scrapy.Request(
                url=f'https://service.mydigilearn.id/pathway/list?limit=50&page={next_page}',
                callback=self.parse,
                headers={
                    'Authorization': auth
                }
            )
    
    def parse_2(self, response):
        resp = json.loads(response.body)
        item = resp.get('result').get('detail')
        yield {
            'title': item.get('title'),
            'description': re.sub(CLEANR, '', item.get('description')) if item.get('description') else item.get('title'),
            'url': f'https://www.mydigilearn.id/pathway/{item.get("id")}',
            'img_url': item.get('image_desktop'),
            'content_type': 'digilearn',
            'published_date': item.get('created_at') if item.get('created_at') else datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'elastic': 0,
            'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }