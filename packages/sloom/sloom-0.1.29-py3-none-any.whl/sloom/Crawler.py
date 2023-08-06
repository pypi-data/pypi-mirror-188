from .Fetcher import Fetcher
from .Scraper import Scraper
from .Response import Response
from .RequestError import RequestError
from .Core.Terminal import Terminal

class Crawler:
    def __init__(self, root) -> None:
        self.root = root

    def crawl(self):
        fetch = Fetcher()
        response = fetch.get_page(self.root)
        if self.isError(response): 
            Terminal.error("Error at root")
            return

        scraper = Scraper(response)

        href = scraper.gethref()
        print(href)
    
    def isError(self, response): return isinstance(response, RequestError)

