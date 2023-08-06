URL_PREFIX = "https://"


class href:
    def __init__(self, string, origin, subdomain) -> None:
        self.content = string
        self.origin = origin
        self.subdomain = subdomain
    
    def url(self): 
        url = self.subdomain + "." + self.origin + self.content
        try:
            scheme = self.content.split(":")[0]
            if scheme == "https": return self.content
            else: return url
        except:
            return url

    def __str__(self) -> str:
        return self.url()