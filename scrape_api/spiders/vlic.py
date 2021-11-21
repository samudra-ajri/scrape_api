# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.utils.project import get_project_settings
from datetime import datetime


class VlicSpider(scrapy.Spider):
    global key, channel_id
    settings = get_project_settings()
    
    name = 'vlic'
    allowed_domains = ['youtube.googleapis.com']

    key = settings.get('YOUTUBE_API_KEY')
    channel_id = settings.get('YOUTUBE_CHANNEL_ID_VLIC')
    
    start_urls = [f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&type=video&channelId={channel_id}&key={key}']

    def parse(self, response):
        resp = json.loads(response.body)
        items = resp.get('items')
        for item in items:
            yield {
                'title': item.get('snippet').get('title'),
                'description': item.get('snippet').get('description').replace('...',''),
                'url': f'https://www.youtube.com/watch?v={item.get("id").get("videoId")}',
                'img_url': item.get('snippet').get('thumbnails').get('medium').get('url'),
                'content_type': 'vlic',
                'published_date': item.get('snippet').get('publishTime'),
                'elastic': 0,
                'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        
        next_page = resp.get('nextPageToken')
        if next_page:
            yield scrapy.Request(
                url=f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&type=video&channelId={channel_id}&pageToken={next_page}&key={key}',
                callback=self.parse
            )