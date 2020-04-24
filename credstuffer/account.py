import os
import requests
import logging
import random
from http.client import HTTPConnection
from abc import ABC, abstractmethod

user_agent_list = [
     #  Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
     #  Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


class Account(ABC):
    """ Abstract Base Class Account to provide basic methods for account specific attributes

    """
    def __init__(self):
        self.logger = logging.getLogger('credstuffer')

        self.root_dir = os.path.dirname(os.path.abspath(__file__))

        self.session = requests.Session()
        self.proxy_test_session = requests.Session()
        self.proxy_test_headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'User-Agent': random.choice(user_agent_list),
            'Accept': 'application/json, text/plain, */*',
        }
        self.login_request_timeout = 4
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'User-Agent': random.choice(user_agent_list),
            'Accept': 'application/json, text/plain, */*',
        }
        self.proxy_test_url = 'http://www.google.com'
        self.proxy_test_timeout = 2

        self.filename = 'cracked_'

    def __del__(self):
        """destructor"""

        self.session.close()

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

            proxy_test_response = self.proxy_test_session.get(self.proxy_test_url, headers=self.proxy_test_headers,
                                                              timeout=self.proxy_test_timeout, allow_redirects=True)
            if proxy_test_response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            return False
        except Exception as ex:
            self.logger.error(ex)
            return False

    def is_internet_available(self):
        """ checks if internet is available with a head request to google.com

        :return: True if internet is available, else False
        """

        conn = HTTPConnection("www.google.com", timeout=2)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except Exception as ex:
            return False

    def set_random_user_agent(self):
        """ sets an user agent from list

        """
        self.logger.info("Renew the user-agent for the request")
        self.headers['User-Agent'] = random.choice(user_agent_list)

