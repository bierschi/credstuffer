import logging
from credstuffer import UserAccount


class Instagram(UserAccount):
    """ class Instagram to provide basic methods for credstuffing instagram.com

    USAGE:
            instagram = Instagram()

    """
    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Comunio')

        # init base class
        super().__init__()


    def login(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        print("instagram")
        pass

    def set_proxy(self, proxy):
        """

        :return:
        """
        pass
