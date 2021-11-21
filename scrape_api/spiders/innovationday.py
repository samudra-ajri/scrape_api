# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.utils.project import get_project_settings
from scrapy.selector import Selector
from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import datetime


class InnovationdaySpider(scrapy.Spider):
    global CLEANR

    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\r\n')
    
    name = 'innovationday'
    allowed_domains = ['innovationday.ddbtelkom.id']

    def start_requests(self):
        yield scrapy.Request(
            url='https://innovationday.ddbtelkom.id/wp-json/elementor-pro/v1/posts-widget?post_id=526&element_id=15adee0&page=1',
            callback=self.parse,
        )

    def parse(self, response):
        resp = json.loads(response.body)
        items = resp.get('content')

        raw_sites = response.xpath('//a[not(@class)]/@href').getall()
        sites = []
        for raw_site in raw_sites:
            raw_site = raw_site.replace('\\', '')
            raw_site = raw_site.replace('"', '')
            sites.append(raw_site)
        
        for site in sites:
            yield scrapy.Request(
                url=site,
                callback=self.parse_2
            )

        if items != '':
            parsed_url = urlparse(response.request.url)
            next_page = int(parse_qs(parsed_url.query)['page'][0]) + 1

            yield scrapy.Request(
                url=f'https://innovationday.ddbtelkom.id/wp-json/elementor-pro/v1/posts-widget?post_id=526&element_id=15adee0&page={next_page}',
                callback=self.parse
            )

    def parse_2(self, response):
        title = response.xpath("//div[@data-id='3a1ee1f3']/div/h2/text()").get()
        description = " ".join(response.xpath("//div[@data-id='7b7e3a60']/div/h2/text()").getall())
        published_date = response.xpath("//div[@data-id='590e1761']/div/h2/text()").get().split(' | ')[0]

        yield {
            'title': title.strip() if title else response.request.url,
            'description': re.sub(CLEANR, '', description.strip()) if description else title,
            'url': response.request.url,
            'img_url': '',
            'content_type': 'innovationday',
            'published_date': published_date if published_date else datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'elastic': 0,
            'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }