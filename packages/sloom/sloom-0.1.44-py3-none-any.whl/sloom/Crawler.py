from .Fetcher import Fetcher
from .Scraper import Scraper
from .RequestError import RequestError
from .Core.Terminal import Terminal

class Crawler:
    def __init__(self, root) -> None:
        self.root = root
        self.fetcher = Fetcher


    def crawl(self):
        fetch = Fetcher()
        response = fetch.get_page(self.root)
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
        list_href.forEach(lambda x: Terminal.found(x))
        responses = self.fetcher.get_all_pages(list_href)
        responses.removeErrors()
        return responses
    
    def isError(self, response): return isinstance(response, RequestError)

