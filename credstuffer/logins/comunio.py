import logging
import requests
from credstuffer import UserAccount
from credstuffer.exceptions import ProxyNotSetError, ProxyMaxRequestError, ProxyBadConnectionError


class Comunio(UserAccount):
    """ class Comunio to provide basic methods for credstuffing comunio.de

    USAGE:
            comunio = Comunio()

    """
    def __init__(self, max_requests=10):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Comunio')

        # init base class
        super().__init__()

        self.headers.update({
            'Origin': 'http://www.comunio.de',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://www.comunio.de/home',
            })

        self.comunio_login_url = 'https://api.comunio.de/login'
        self.max_requests = max_requests
        self.request_counter = 0

    def login(self, username, password):
        """ requests given login data to the account

        :return: None or request Response
        """
        login_form = [('username', username), ('password', password), ]

        # check if proxy is set
        if self.session.proxies:

            # check if we need a new proxy
            if self.request_counter < self.max_requests:

                try:
                    request_login = self.session.post(self.comunio_login_url, headers=self.headers, data=login_form, timeout=self.login_request_timeout, allow_redirects=False)
                    self.request_counter += 1
                    self.logger.info("request comunio with username: {}, password: {}, proxy: {}".format(username, password, self.session.proxies['http']))
                except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                    #self.logger.error(e)
                    raise ProxyBadConnectionError("Proxy Bad Connection")
            else:
                # raise Error to renew Proxy
                raise ProxyMaxRequestError("Max number of proxy requests reached!")
        else:
            raise ProxyNotSetError("No Proxy was set!")

        return request_login

    def set_proxy(self, proxy):
        """ sets a proxy

        """
        if isinstance(proxy, dict):
            alive = self.is_proxy_alive(proxy=proxy)
            if alive:
                self.logger.info("set proxy to {}".format(proxy['http']))
                self.session.proxies = proxy
            else:
                raise ProxyBadConnectionError("Renew proxy due to bad connection!")
        else:
            raise TypeError("proxy must be type of dictionary!")

