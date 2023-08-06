from .Core.Terminal import *
from .ResponseType import *

class Response(ResponseType):
    def __init__(self, text, url) -> None:
        self.text = text
        self.url = url
        self.origin = self.getOrigin()
        self.debug_init()
    
    def getOrigin(self):
        try: 
            split = self.url.split(".")
            domain = split[1]
            TLD = split.split("/")[0]
            return domain + "." + TLD
        except:
            return None
    
    def debug_init(self):
        Terminal.put(f"{self.url} - {bcolors.OKGREEN}success{bcolors.ENDC}")
    
    def __str__(self) -> None:
        return f"Response({self.url[0:10]})"