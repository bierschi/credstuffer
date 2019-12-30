import argparse
from credstuffer.utils.logger import Logger
from credstuffer.stuffing import Stuffing
from credstuffer import __version__
from credstuffer.logins import Comunio


class Credstuffer:

    def __init__(self, account, nsmtp=None, nport=None, nsender=None, nreceiver=None, npassword=None, filepath=None, **dbparams):

        self.account = account
        self.smtp = nsmtp
        self.port = nport
        self.sender = nsender
        self.receiver = nreceiver
        self.password = npassword
        self.filepath = filepath
        self.dbparams = dbparams

        self.accounts = list()
        # create account instances
        if self.account == 'comunio':

            comunio = Comunio(max_requests=500000, SMTP=self.smtp, PORT=self.port, SENDER=self.sender,
                              RECEIVER=self.receiver, PASSWORD=self.password, notify='mail')

            self.accounts.append(comunio)

            if self.filepath is not None:
                stuffer = Stuffing(accounts=self.accounts, filepath=self.filepath)
            else:
                stuffer = Stuffing(accounts=self.accounts, **self.dbparams)

            stuffer.run()


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

    if args.subcommand == 'file':
        if args.path is not None:
            logger.info("process credential file")

            credstuffer = Credstuffer(account=args.account, nsmtp=args.Nsmtp, nport=args.Nport, nsender=args.Nsender,
                                      nreceiver=args.Nreceiver, npassword=args.Npassword, filepath=args.path)
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
        dbparams = {'host': host, 'port': port, 'username': username, 'password': password, 'dbname': dbname}

        credstuffer = Credstuffer(account=args.account, nsmtp=args.Nsmtp, nport=args.Nport, nsender=args.Nsender,
                                  nreceiver=args.Nreceiver, npassword=args.Npassword, **dbparams)


if __name__ == '__main__':
    main()
