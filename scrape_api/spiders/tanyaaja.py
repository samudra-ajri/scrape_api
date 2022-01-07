# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.utils.project import get_project_settings
from datetime import datetime

class TanyaajaSpider(scrapy.Spider):
    global auth, CLEANR
    settings = get_project_settings()

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    auth = settings.get('TANYAAJA_AUTH_HEADER')
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\r\n')

    name = 'tanyaaja'
    allowed_domains = ['tanya-aja.com']

    def start_requests(self):
        yield scrapy.Request(
            url='https://tanya-aja.com/api/taja/categories',
            callback=self.parse,
            headers={
                'Authorization': auth
            }
        )

    def parse(self, response):
        resp = json.loads(response.body)
        items = resp
        sites = []
        for item in items:
            url = f'https://tanya-aja.com/api/taja/bycategory/{item.get("id")}'
            sites.append(url)
        
        for site in sites:
            yield scrapy.Request(
                url=site,
                callback=self.parse_2,
                headers={
                    'Authorization': auth
                }
            )
    
    def parse_2(self, response):
        resp = json.loads(response.body)
        items = resp.get('questions').get('data')
        sites = []
        for item in items:
            url = f'https://tanya-aja.com/api/taja/question/{item.get("id")}'
            sites.append(url)
        
        for site in sites:
            yield scrapy.Request(
                url=site,
                callback=self.parse_3,
                headers={
                    'Authorization': auth
                }
            )
        
        next_page = resp.get('questions').get('next_page_url')
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_2,
                headers={
                    'Authorization': auth
                }
            )
    
    def parse_3(self, response):
        resp = json.loads(response.body)
        item = resp
        date = datetime.strptime(item.get('created_at'), '%Y-%m-%d %H:%M:%S')
        yield {
            'title': f'Tanya Aja Question: {item.get("id")}',
            'description': re.sub(CLEANR, '', item.get('text_content')) if item.get('text_content') else item.get('title'),
            'url': f'https://app.tanya-aja.com/detail-question/{item.get("id")}',
            'img_url': item.get('image_content'),
            'content_type': 'tanyaaja',
            'published_date': date.isoformat()+'Z' if item.get('created_at') else datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'elastic': 0,
            'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }