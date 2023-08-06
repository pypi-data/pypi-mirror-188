from .Core.Terminal import *
from .ResponseType import *

class Response(ResponseType):
    def __init__(self, text, url) -> None:
        self.text = text
        self.url = url
        self.subdomain, self.origin = self.getOrigin()
        
        self.debug_init()
    
    def getOrigin(self):
        try: 
            split = self.url.split(".")
            domain = split[1]
            subdomain = split[0]
            TLD = split[2].split("/")[0]
            return subdomain, domain + "." + TLD
        except:
            return None, None
    
    def debug_init(self):
        Terminal.put(f"{self.url} - {bcolors.OKGREEN}success{bcolors.ENDC}")
    
    def __str__(self) -> str:
        return f"Response({self.url[0:10]})"