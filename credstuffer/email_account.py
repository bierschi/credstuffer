import logging
from abc import abstractmethod

from credstuffer import Account


class EmailAccount(Account):
    """ Base class EmailAccount to provide basic methods for accounts with email accounts

    USAGE:
            eaccount = EmailAccount()

    """
    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class EmailAccount')

        # init base class
        super().__init__()

    @abstractmethod
    def login(self, email, password):
        """ abstract method login

        :return: None or request Response
        """
        pass
