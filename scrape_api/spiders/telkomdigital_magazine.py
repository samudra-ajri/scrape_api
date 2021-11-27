# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.utils.project import get_project_settings
from datetime import datetime


class telkomdigitalMagazineSpider(scrapy.Spider):
    global token, uid, client_id, CLEANR
    settings = get_project_settings()

    name = 'telkomdigital_magazine'
    allowed_domains = ['admin.telkomdigital.id']

    token = settings.get('TELKOMDIGITAL_TOKEN')
    uid = settings.get('TELKOMDIGITAL_UID')
    client_id = settings.get('TELKOMDIGITAL_CLIENT_ID')

    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\r\n')

    def start_requests(self):
        yield scrapy.Request(
            url='https://admin.telkomdigital.id/api/v2/magazines?limit=50&page=1',
            callback=self.parse,
            headers={
                'access-token': token,
                'client': client_id,
                'uid': uid
            }
        )

    def parse(self, response):
        resp = json.loads(response.body)
        items = resp.get('magazines')
        sites = []
        for item in items:
            url = f'https://admin.telkomdigital.id/api/v2/magazines/{item.get("id")}'
            sites.append(url)
        
        for site in sites:
            yield scrapy.Request(
                url=site,
                callback=self.parse_2,
                headers={
                    'access-token': token,
                    'client': client_id,
                    'uid': uid
                }
            )

        next_page = resp.get('meta')
        if next_page:
            yield scrapy.Request(
                url=f'https://admin.telkomdigital.id/api/v2/magazines?limit=50&page={next_page}',
                callback=self.parse,
                headers={
                    'access-token': token,
                    'client': client_id,
                    'uid': uid
                }
            )

    def parse_2(self, response):
        resp = json.loads(response.body)
        item = resp.get('magazine')
        yield {
            'title': item.get('title'),
            'description': re.sub(CLEANR, '', item.get('description')) if item.get('description') else item.get('title'),
            'url': f'https://telkomdigital.id/magazine/{item.get("title").lower().replace(" ", "-")}',
            'img_url': f'https://admin.telkomdigital.id{item.get("thumbnail")}',
            'content_type': 'telkomdigital',
            'published_date': item.get('created_at') if item.get('created_at') else datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'elastic': 0,
            'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
