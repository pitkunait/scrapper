import logging
import pickle
from itertools import cycle

import requests
from requests.exceptions import RequestException

from .CrawlerSettings import CrawlerSettings
from .ProxyParser import ProxyParser

logger = logging.getLogger("ProxyCrawler.py")


class ProxyCrawler:

    def __init__(self):
        self.proxy_set = set()
        self.bad_proxies = []
        self.proxy_pool = cycle(self.proxy_set)
        self.proxy_parser: ProxyParser = ProxyParser()
        self.options: CrawlerSettings = CrawlerSettings()
        if self.options.cache_bad_proxies:
            self.retrieve_bad_proxies()
        self.add_proxies()

    def status(self):
        print("Active proxies:", len(self.proxy_set))
        print("Bad proxies:", len(self.bad_proxies))

    def get(self, url, test_function=None):
        proxy = self.get_proxy()
        try:
            logger.debug(f"Sending request using {proxy} to {url}")
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            logger.info(f"{response.status_code}: {url}")
            if response.status_code == 200:
                return response
            else:

                if test_function:
                    if test_function(response):
                        return response
                    else:
                        return self.resend_get(url, proxy)

                return response

        except RequestException:
            return self.resend_get(url, proxy)

    def get_proxy(self):
        return next(self.proxy_pool)

    def cache_all(self):
        self.cache_bad_proxies()

    def cache_bad_proxies(self):
        with open(self.options.BAD_PROXY_PATH, 'wb') as file:
            pickle.dump(self.bad_proxies, file)

    def retrieve_bad_proxies(self):
        try:
            with open(self.options.BAD_PROXY_PATH, 'rb') as f:
                bad_proxies = pickle.load(f)
                if len(bad_proxies) > 0:
                    self.bad_proxies = bad_proxies
        except Exception as e:
            logger.warning(f"Error loading bad proxies cache: {e}")

    def resend_get(self, url, proxy):
        self.remove_proxy(proxy)
        return self.get(url)

    def remove_proxy(self, to_delete):
        self.proxy_set.remove(to_delete)
        logger.info(f"Removing {to_delete}; proxies left: {len(self.proxy_set)}")
        self.bad_proxies.append(to_delete)
        self.proxy_pool = cycle(self.proxy_set)

    def add_proxies(self):
        new_proxies = self.proxy_parser.get_all_proxies()
        for i in new_proxies:
            if i not in self.bad_proxies:
                self.proxy_set.add(i)
        self.proxy_pool = cycle(self.proxy_set)
