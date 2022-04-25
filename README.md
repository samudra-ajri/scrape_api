# Scrape API 

## Overview
This service will scrape the youtube api with specific channel id (VLIC Corpu channel in this example).

## Stack Architechture
1. Python 3.7
2. Scrapy 1.6
3. MongoDB Atlas

## Local development quickstart
Clone the repository
```
$ git clone git@github.com:samudra-ajri/scrape_api.git
```
Enter into the `scrape_api` directory, then install the dependencies
```
$ cd scrape_api
```
Copy the config file and adjust the needs
```
$ copy .env-example .env
fill the .env with your needs
```
Install the dependencies:
```
$ pip install -r requirements.txt
```
Run the service/spiders:
```
$ cd scrape_api
$ scrapy crawl <spider_name>
for example: $ scrapy crawl vlic.py
```

### Stored data checking
Open your favorite mongodb client, then check your mongo_uri.
