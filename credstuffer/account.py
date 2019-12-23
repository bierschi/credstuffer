import requests
import logging
from abc import ABC, abstractmethod


class Account(ABC):
    """ Abstract Base Class Account to provide basic methods for account specific attributes

    """
    def __init__(self):
        self.logger = logging.getLogger('credstuffer')

        self.session = requests.Session()
        self.login_request_timeout = 2
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
        }
        self.proxy_test_url = 'http://www.google.com'
        self.proxy_test_timeout = 2
        #self.session.max_redirects = 100

    @abstractmethod
    def set_proxy(self, proxy):
        """ sets a proxy to the current session

        """
        pass

    def is_proxy_alive(self, proxy):
        """ checks if a proxy is alive

        :param proxy: proxy as ip:port
        :return: True if alive
        """
        try:
            self.session.proxies = proxy
            proxy_test_response = self.session.get(self.proxy_test_url, headers=self.headers, timeout=self.proxy_test_timeout, allow_redirects=False)
            if proxy_test_response.status_code == 200:
                return True
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
            self.logger.error(e)
            return False

    def random_user_agent(self):
        """

        :return:
        """
        pass
