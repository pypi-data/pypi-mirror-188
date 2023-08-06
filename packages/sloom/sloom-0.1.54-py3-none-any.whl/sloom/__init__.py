from .Crawler import Crawler

#Top Level core classes
from .Core.List import List

class Sloom:
    def __init__(self, root) -> None:
        self.root = root
        self.run()
    
    def run(self, root):
        crawler = Crawler(root)
        crawler.crawl()