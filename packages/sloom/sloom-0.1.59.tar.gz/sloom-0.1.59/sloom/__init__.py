from .Crawler import Crawler
from .Fetcher import Fetcher
from .Scraper import Scraper

#Top Level core classes
from .Core.List import List

class _Sloom:
    def __init__(self, url) -> None:
        self.run(url)
    
    def run(self, root):
        crawler = Crawler(root)
        crawler.crawl()

def run(url): _Sloom(url)