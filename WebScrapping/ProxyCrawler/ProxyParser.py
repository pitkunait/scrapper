import requests
from lxml.html import fromstring


class ProxyParser:
    """
    Proxy parser.
    Add staticmethods to this class starting with 'get_proxies_'
    """

    def __init__(self):
        pass

    def get_all_proxies(self):
        all_proxies = set()

        for i in dir(self):
            if i.startswith('get_proxies_'):
                try:
                    method = getattr(self, i)
                    all_proxies = all_proxies.union(method())
                except Exception as e:
                    print(e)

        if len(all_proxies) < 1:
            raise ValueError("No proxies obtained")

        return all_proxies

    @staticmethod
    def get_proxies_1():
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:79]:
            # if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
        return proxies
