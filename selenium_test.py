import scrapy
from pprint import pprint
from pathlib import Path
import json
usernames = ['altnbgn']
proxy = 'server:port'
output = {}


class QuotesSpider(scrapy.Spider):
    def start_requests(self, url):
        return scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

def main():
    user_name = 'altnbgn'
    profile_url = f'https://www.instagram.com/{user_name}/?hl=en'


if __name__ == '__main__':
    main()
    pprint(output)