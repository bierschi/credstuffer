import logging
from credstuffer import UserAccount


class Instagram(UserAccount):
    """ class Instagram to provide basic methods for credstuffing instagram.com

    USAGE:
            instagram = Instagram()

    """
    usernames = list()

    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Comunio')

        # init base class
        super().__init__()

    def set_usernames(self, usernames):
        """ sets usernames for instagram account

        :param usernames: list of usernames
        """
        self.usernames = usernames

    def login(self, password):
        """

        :param username:
        :param password:
        :return:
        """
        print("instagram")
        pass

    def notifyer(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        pass

    def set_proxy(self, proxy):
        """

        :return:
        """
        pass
