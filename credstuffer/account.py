import requests
from abc import ABC, abstractmethod


class Account(ABC):
    """ Abstract Base Class Account to provide basic methods for account specific attributes

    """
    def __init__(self):

        self.session = requests.Session()
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
        }

    @abstractmethod
    def set_proxy(self, proxy):
        """

        :return:
        """
        pass

    def random_user_agent(self):
        """

        :return:
        """
        pass
