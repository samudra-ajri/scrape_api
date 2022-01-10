# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.utils.project import get_project_settings
from scrapy.selector import Selector
from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import datetime


class HcwikiSpider(scrapy.Spider):
    global auth, CLEANR
    settings = get_project_settings()

    auth = settings.get('HCWIKI_SESSION')
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\r\t\n')

    name = 'hcwiki'
    allowed_domains = ['hcwiki.telkom.co.id']

    def start_requests(self):
        yield scrapy.Request(
            url='https://hcwiki.telkom.co.id/home',
            callback=self.parse,
            cookies={
                'sessionid': auth,
            }
        )

    def parse(self, response):
        global last_visited
        resp = response
        sites = resp.xpath("//div[@class='panel-body']/a[starts-with(@href, '/search/')]/@href").getall()
        for site in sites:
            yield scrapy.Request(
                url=f'https://hcwiki.telkom.co.id{site}',
                callback=self.parse_2,
                cookies={
                    'sessionid': auth
                }
            )

    def parse_2(self, response):
        resp = response
        sites = resp.xpath("//div[@class='row']/h3/a/@href").getall()
        for site in sites:
            yield scrapy.Request(
                url=f'https://hcwiki.telkom.co.id{site}',
                callback=self.parse_3,
                cookies={
                    'sessionid': auth
                }
            )
        
        next_page = resp.xpath("//a[contains(text(),'Next')]/@href").get()
        if next_page:
            yield scrapy.Request(
                url=response.request.url.split('?')[0]+next_page,
                callback=self.parse_2,
                headers={
                    'sessionid': auth
                }
            )

    def parse_3(self, response):
        title = response.xpath("//title/text()").get()
        description = (" ".join(response.xpath('//div[@id="save"]/descendant::*/text()').getall())).replace('\n',"").replace('\r',"").replace('\t',"").replace('\xa0',"")
        date = datetime.strptime(response.xpath('//p[contains(text(),"Published Date")]/text()').get(), 'Published Date: %b %d, %Y')
        yield {
            'title': title,
            'description': re.sub(CLEANR, '', description.strip()) if description else title,
            'url': response.request.url,
            'img_url': None,
            'content_type': 'hcwiki',
            'published_date': date.isoformat()+'Z' if date else datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'elastic': 0,
            'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
