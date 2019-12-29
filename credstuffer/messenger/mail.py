import ssl
import logging
import smtplib
from email.message import EmailMessage


class Mail:
    """ class Mail to provide sending credentials to specific email adress

    USAGE:
            mail = Mail(smtp_server="smtp.web.de", port=587, sender=sender@web.de, receiver=receiver@web.de, debug=False)
            mail.login(username='', password='')
            mail.send()
    """
    def __init__(self, smtp_server, port, sender, receiver, debug=False):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Mail')

        self.smtp_server = smtp_server
        self.port = port
        self.sender = sender
        self.receiver = receiver

        self.server = smtplib.SMTP(self.smtp_server, self.port)
        self.context = ssl.create_default_context()
        self.server.starttls(context=self.context)

        if debug:
            self.server.set_debuglevel(True)

        self.msg = EmailMessage()
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

    def __del__(self):
        """ destructor

        """
        if self.server:
            self.server.quit()

    def login(self, username, password):
        """ login to email account with username and password

        """
        self.server.login(user=username, password=password)

    def set_subject(self, subject):
        """ sets the subject for the email

        :param subject: subject in email
        """
        self.msg['Subject'] = subject

    def set_body(self, body):
        """ sets the body for the email

        :param body: body content in email
        """
        self.msg.set_content(body)

    def send(self):
        """ sends the email

        """
        self.server.sendmail(self.sender, self.receiver, self.msg.as_string())

