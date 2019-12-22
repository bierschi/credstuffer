import logging
from abc import abstractmethod

from credstuffer import Account


class UserAccount(Account):
    """ Base class UserAccount to provide basic methods for accounts with username logins

    USAGE:
            UserAccount

    """
    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class UserAccount')

        # init base class
        super().__init__()

    @abstractmethod
    def login(self, username, password):
        """ abstract method login

        :return: None or request Response
        """
        pass
