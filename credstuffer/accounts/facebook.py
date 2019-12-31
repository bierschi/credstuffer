import logging
from credstuffer import EmailAccount


class Facebook(EmailAccount):
    """ class Facebook to provide basic methods for credstuffing facebook.com

    USAGE:
            facebook = Facebook()

    """
    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Facebook')

        # init base class
        super().__init__()

    def login(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        print("facebook")
        pass

    def set_proxy(self, proxy):
        """

        :return:
        """
        pass
