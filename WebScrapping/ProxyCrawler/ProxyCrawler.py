import logging
import pickle
import threading
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
from typing import Union

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
        self._lock = threading.Lock()
        if self.options.cache_bad_proxies:
            self.retrieve_bad_proxies()
        self.add_proxies()

        self.executor: Union[ThreadPoolExecutor, None] = None
        self.futures = []
        self.err_count = 0

    def status(self):
        print("Active proxies:", len(self.proxy_set))
        print("Bad proxies:", len(self.bad_proxies))

    def start_executor(self, workers=10):
        self.futures = []
        self.executor = ThreadPoolExecutor(max_workers=workers)

    def run_parallel(self, function, *args):
        future = self.executor.submit(function, *args)
        self.futures.append(future)

    def stop_executor(self):
        self.executor.shutdown(wait=False)
        for i in self.futures:
            i.cancel()

    def get(self, url, test_function=None):
        proxy = self.get_proxy()
        try:
            logger.debug(f"Sending request using {proxy} to {url}")
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            logger.info(f"{response.status_code}: {url}")

            if test_function:
                if test_function(response):
                    print(url, "passed check")
                    return response
                else:
                    return self.resend_get(url, proxy, test_function)

            return response

        except RequestException:
            return self.resend_get(url, proxy, test_function)

    def get_proxy(self):
        with self._lock:
            try:
                proxy = next(self.proxy_pool)
                self.err_count = 0
                return proxy
            except StopIteration:
                self.err_count += 1
                self.add_proxies()
                if self.err_count > self.options.ERR_MAX_COUNT:
                    raise RecursionError("No proxies left")
                return self.get_proxy()

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

    def resend_get(self, url, proxy, test_function=None):
        self.remove_proxy(proxy)
        return self.get(url, test_function)

    def remove_proxy(self, to_delete):
        with self._lock:
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
