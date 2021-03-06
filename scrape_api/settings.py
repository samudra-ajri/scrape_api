# -*- coding: utf-8 -*-
from decouple import config

# Scrapy settings for scrape_api project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrape_api'

SPIDER_MODULES = ['scrape_api.spiders']
NEWSPIDER_MODULE = 'scrape_api.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrape_api (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrape_api.middlewares.ScrapeApiSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrape_api.middlewares.ScrapeApiDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'scrape_api.pipelines.MongodbPipeline': 300,
   'scrape_api.pipelines.DuplicatesPipeline': 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Yotube configuration
YOUTUBE_API_KEY=config('YOUTUBE_API_KEY')
YOUTUBE_CHANNEL_ID_VLIC=config('YOUTUBE_CHANNEL_ID_VLIC')
YOUTUBE_CHANNEL_ID_ITDR=config('YOUTUBE_CHANNEL_ID_ITDR')
YOUTUBE_CHANNEL_ID_TELKOMDIGITAL=config('YOUTUBE_CHANNEL_ID_TELKOMDIGITAL')
YOUTUBE_CHANNEL_ID_LIVINGTELKOM=config('YOUTUBE_CHANNEL_ID_LIVINGTELKOM')
YOUTUBE_CHANNEL_ID_TELKOMOFFICIALL=config('YOUTUBE_CHANNEL_ID_TELKOMOFFICIALL')

# Digilearn configuration
DIGILEARN_AUTH_HEADER=config('DIGILEARN_AUTH_HEADER')

# Telkomdigital configuration
TELKOMDIGITAL_TOKEN=config('TELKOMDIGITAL_TOKEN')
TELKOMDIGITAL_CLIENT_ID=config('TELKOMDIGITAL_CLIENT_ID')
TELKOMDIGITAL_UID=config('TELKOMDIGITAL_UID')

# MongoDB configuration
MONGO_URI=config('MONGO_URI')
MONGO_DATABASE=config('MONGO_DATABASE')

# Tanyaaja configuration
TANYAAJA_AUTH_HEADER=config('TANYAAJA_AUTH_HEADER')

# Digitallearning configuration
DIGITALLEARNING_SESSION=config('DIGITALLEARNING_SESSION')

# Hcwiki configuration
HCWIKI_SESSION=config('HCWIKI_SESSION')