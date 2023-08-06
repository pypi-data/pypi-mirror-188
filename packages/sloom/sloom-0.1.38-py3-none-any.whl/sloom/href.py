URL_PREFIX = "https://www."


class href:
    def __init__(self, string, origin) -> None:
        self.content = string
        self.origin = origin
    
    def url(self): 
        url = URL_PREFIX + self.origin + self.content
        try:
            scheme = self.content.split(":")[0]
            if scheme == "https": return self.content
            else: return url
        except:
            return url

    def __str__(self) -> str:
        return self.content