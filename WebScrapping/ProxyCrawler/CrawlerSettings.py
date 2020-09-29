from pathlib import Path


class CrawlerSettings:

    def __init__(self):
        self.cache_bad_proxies = True
        self.CACHE_PATH = str(Path(__file__).parent.absolute()) + "/cache"
        self.BAD_PROXY_PATH = self.CACHE_PATH + "/bad_proxies.pickle"
        self.ERR_MAX_COUNT = 3
