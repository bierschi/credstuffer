import logging

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

        self.usernames = [user.strip() for user in usernames]  # strip leading and trailing whitespaces
        self.accounts = accounts

        for account in self.accounts:
            account.set_usernames(usernames=self.usernames)

    def database_stuffing(self, schemas, tables, **dbparams):
        """ creates the DatabaseStuffer instance and starts the run thread

        """
        if all(el is not None for el in [schemas, tables]):
            stuffer = DatabaseStuffer(account=self.accounts[0], schemas=schemas, tables=tables, **dbparams)
            stuffer.start()
        else:
            self.logger.error("Argument schemas or tables is None, can not start DatabaseStuffer")

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

