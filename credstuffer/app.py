import argparse
import logging
from credstuffer.utils.logger import Logger
from credstuffer.algorithm import Algorithm
from credstuffer import __version__
from credstuffer.accounts import Comunio


class Credstuffer:
    """ class Credstuffer

    USAGE:
            credstuffer = Credstuffer()

    """
    def __init__(self, account, filepath=None, **params):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Credstuffer')

        self.account = account
        self.filepath = filepath
        self.mailparams = dict()
        self.dbparams = dict()

        if ('smtp' and 'port' and 'sender' and 'receiver' and 'password') in params['mail'].keys():
            self.mailparams.update(params['mail'])
        else:
            self.logger.error("No mail parameters provided!")

        if ('host' and 'port' and 'username' and 'password' and 'dbname') in params['database'].keys():
            self.dbparams.update(params['database'])
        else:
            self.logger.error("No database parameters provided!")

        self.accounts = list()
        # create account instances
        if self.account == 'comunio':

            comunio = Comunio(max_requests=500000, notify='mail', **self.mailparams)

            self.accounts.append(comunio)

            if self.filepath is not None:
                algo = Algorithm(accounts=self.accounts, filepath=self.filepath)
            else:
                algo = Algorithm(accounts=self.accounts, **self.dbparams)

            algo.execute()


def main():

    # parse arguments for credstuffer
    usage1 = "credstuffer instagram database --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname postgres"
    usage2 = "credstuffer facebook file --path /home/john/credentials.txt"

    description = "console script for application credstuffer \n\nUsage:\n    {}\n    {}".format(usage1, usage2)
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

    parser_notifyer = parser.add_argument_group('Notification', 'Define arguments for Mail or Telegram Notification')
    parser_notifyer.add_argument('--Nsmtp', type=str, help='SMTP email server')
    parser_notifyer.add_argument('--Nport', type=int, help='SMTP Port')
    parser_notifyer.add_argument('--Nsender', type=str, help='email from sender')
    parser_notifyer.add_argument('--Nreceiver', type=str, help='email from receiver')
    parser_notifyer.add_argument('--Npassword', type=str, help='password from sender email')

    parser.add_argument('-v', '--version', action='version', version=__version__, help='show the current version')

    args = parser.parse_args()

    # set up logger instance
    logger = Logger(name='credstuffer', level='info', log_folder='/var/log/')
    logger.info("start application credstuffer")

    params = dict()
    nsmtp = args.Nsmtp
    nport = args.Nport
    nsender = args.Nsender
    nreceiver = args.Nreceiver
    npassword = args.Npassword

    params.setdefault('mail', {'smtp': nsmtp, 'port': nport, 'sender': nsender, 'receiver': nreceiver,
                               'password': npassword})

    if args.subcommand == 'file':
        if args.path is not None:
            logger.info("process credential file")

            credstuffer = Credstuffer(account=args.account, filepath=args.path, **params)
        else:
            # currently not supported
            logger.info("process credential directory")
    else:
        logger.info("process database parameters")
        host = args.host
        port = args.port
        username = args.user
        password = args.password
        dbname = args.dbname
        params.setdefault('database', {'host': host, 'port': port, 'username': username, 'password': password,
                                       'dbname': dbname})

        credstuffer = Credstuffer(account=args.account, **params)


if __name__ == '__main__':
    main()
