import logging
from time import sleep
from credstuffer.proxy import Proxy
from credstuffer.exceptions import ProxyMaxRequestError, ProxyNotSetError, ProxyBadConnectionError, \
    InternetConnectionError


class Stuffer:
    """ Base class Stuffer to provide basic methods for the stuffing algorithm

    USAGE:
            stuffer = Stuffer(account=account, timeout_ms=50)

    """
    def __init__(self, account, timeout_ms=50):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('Create class Stuffer')

        self.account = account

        self.proxy = Proxy(timeout_ms=timeout_ms)

    def set_account_proxy(self):
        """ sets a proxy for the given account

        :param account: account instance
        """

        proxy_alive = False
        while not proxy_alive:
            proxy = self.__get_proxy_dict()
            if self.account.is_proxy_alive(proxy=proxy):
                try:
                    self.account.set_proxy(proxy=proxy)
                    # proxy was renewed therefore the user agent shall be renewed as well
                    self.account.set_random_user_agent()
                    proxy_alive = True
                except TypeError as ex:
                    self.logger.error(ex)

    def account_login(self, password):
        """ executes the account login with given password

        """
        try:
            self.account.login(password)
        except (ProxyMaxRequestError, ProxyBadConnectionError, ProxyNotSetError) as ex:
            self.logger.error("{}".format(ex))
            self.set_account_proxy()
            self.account_login(password=password)
        except InternetConnectionError as ex:
            self.logger.error("{}".format(ex))
            sleep(10)
            self.account_login(password=password)
        except Exception as ex:
            self.logger.error("FATAL ERROR: {}".format(ex))
            self.set_account_proxy()
            self.account_login(password=password)

    def __get_proxy_dict(self):
        """ get proxy dictionary

        :return: dict with 'http' proxy
        """
        proxy = self.proxy.get()
        http_proxy = proxy
        https_proxy = proxy

        return {'http': http_proxy}
