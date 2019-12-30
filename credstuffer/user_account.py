import logging
from abc import abstractmethod

from credstuffer import Account


class UserAccount(Account):
    """ Base class UserAccount to provide basic methods for accounts with username logins

    USAGE:
            UserAccount

    """
    def __init__(self, name=None, notify=None, SMTP=None, PORT=None, SENDER=None, RECEIVER=None, PASSWORD=None):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class UserAccount')

        # init base class
        super().__init__(name=name, notify=notify, SMTP=SMTP, PORT=PORT, SENDER=SENDER, RECEIVER=RECEIVER, PASSWORD=PASSWORD)

    @abstractmethod
    def set_usernames(self, usernames):
        """ abstract method set_usernames

        :param usernames: list of usernames
        """
        pass

    @abstractmethod
    def login(self, password):
        """ abstract method login

        :return: None or request Response
        """
        pass

