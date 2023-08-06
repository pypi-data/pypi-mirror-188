from .Fetcher import Fetcher
from .Scraper import Scraper
from .RequestError import RequestError
from .Core.Terminal import Terminal

class Crawler:
    def __init__(self, root) -> None:
        self.root = root
        self.fetcher = Fetcher()
        self.visitedSites = set()


    def crawl(self):
        response = self.fetcher.get_page(self.root)
        if self.isError(response): 
            Terminal.error("Error at root")
            return
        responses = self._crawling_(response)
        self._crawl(responses)

    
    def _crawl(self, responses):
        for response in responses.contents:
            urls = self._crawling_(response)
            if urls: self._crawl(urls)
    
    def _crawling_(self, response):
        scraper = Scraper(response)
        list_href = scraper.gethref()
        if list_href.count == 0 or not list_href: return None
        list_href.map(lambda x: x.url())
        list_href.filter(self.visitedSites)
        responses = self.fetcher.get_all_pages(list_href.contents)
        responses.removeErrors()
        return responses

    def visited(self, url):
        if url in self.visitedSites: return False
        else:
            Terminal.found(url)
            self.visitedSites.add(url)
            return True
    
    def isError(self, response): return isinstance(response, RequestError)

