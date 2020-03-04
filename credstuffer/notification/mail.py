import ssl
import logging
import smtplib
from email.message import EmailMessage

from credstuffer.exceptions import MailMessageError


class Mail:
    """ class Mail to provide sending credentials to specific email address

    USAGE:
            mail = Mail(smtp_server="smtp.web.de", port=587, debug=False)
            mail.login(username='', password='')
            mail.send(username, password, receiver)
    """
    def __init__(self, smtp_server, port, debug=False):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Mail')

        self.smtp_server = smtp_server
        self.port = port
        self.sender = None
        self.__password = None
        self.server = smtplib.SMTP(self.smtp_server, self.port)  # implicit connecting to server
        self.context = ssl.create_default_context()
        self.server.starttls(context=self.context)

        if debug:
            self.server.set_debuglevel(True)

        self.msg = None

    def connect(self, smtp_server, port):
        """ connects to the smtp server with given port

        :param smtp_server: smtp server host
        :param port: port
        """
        self.logger.info("Connect to mail server")
        self.server.connect(host=smtp_server, port=port)

        self.context = ssl.create_default_context()
        self.server.starttls(context=self.context)

    def login(self, username, password):
        """ login to email account with username and password

        :return True if login was successful, else False
        """
        try:
            ret = self.server.login(user=username, password=password)
        except smtplib.SMTPServerDisconnected as ex:
            self.logger.error("Server disconnected, connecting again: {}".format(ex))
            self.connect(smtp_server=self.smtp_server, port=self.port)
            return self.login(username=username, password=password)
        return ret[0] == 235  # authentication was successful

    def quit(self):
        """ quits the server connection cleanly

        """
        self.server.quit()

    def new_message(self):
        """ creates a new EmailMessage object

        """
        self.msg = EmailMessage()

    def set_subject(self, subject):
        """ sets the subject for the email

        :param subject: subject in email
        """
        if self.msg is not None:
            self.msg['Subject'] = subject
        else:
            raise MailMessageError("No Mail Message was set! Call 'new_message' first")

    def set_body(self, body):
        """ sets the body for the email

        :param body: body content in email
        """
        if self.msg is not None:
            self.msg.set_content(body)
        else:
            raise MailMessageError("No Mail Message was set! Call 'new_message' first")

    def send(self, username, password, receiver):
        """ sends the email to the receiver

        """
        if self.msg is not None:
            self.msg['From'] = username
            self.msg['To'] = receiver
            try:
                self.connect(smtp_server=self.smtp_server, port=self.port)

                if self.login(username=username, password=password):
                    self.logger.info("Authentication to Mail Server was successful")
                    self.server.sendmail(username, receiver, self.msg.as_string())
                else:
                    self.logger.error("Authentication to Mail Server failed!")
            except (smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused) as ex:
                self.logger.error("Failed to send the mail: {}".format(ex))
            finally:
                self.quit()

            self.msg.clear()
        else:
            raise MailMessageError("No Mail Message was set! Call 'new_message' first")

