import argparse
from credstuffer.utils.logger import Logger
from credstuffer.stuffing import Stuffing


def main():

    # parse arguments for credstuffer
    usage1 = "credstuffer instagram database --host 192.168.1.2 --port 5432 --user john --password test1234 --dbname postgres"
    usage2 = "credstuffer facebook file --path /home/john/credentials.txt"

    description = "console script for application credstuffer \n\nUsage:\n    {}\n    {}".format(usage1, usage2)
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

    # account required
    parser.add_argument('account', choices=['comunio', 'instagram', 'facebook'], help='The account you want to stuffing')
    subparsers = parser.add_subparsers(dest='subcommand', help='File or database subcommands')

    # parser for file parameters
    parser_file = subparsers.add_parser('file', help='Path to a single file or a directory')
    parser_file.add_argument('-p', '--path', type=str, help='Path to a single file')
    parser_file.add_argument('-d', '--dir',  type=str, help='Path to a directory')

    # parser for database parameters
    parser_database = subparsers.add_parser('database', help='Database connection arguments')
    parser_database.add_argument('-H', '--host',     type=str, help='Hostname for the database connection', required=True)
    parser_database.add_argument('-P', '--port',     type=str, help='Port for the database connection', required=True)
    parser_database.add_argument('-U', '--user',     type=str, help='User for the database connection', required=True)
    parser_database.add_argument('-p', '--password', type=str, help='Password from the user', required=True)
    parser_database.add_argument('-DB', '--dbname',  type=str, help='Database name', required=True)

    args = parser.parse_args()

    # set up logger instance
    logger = Logger(name='credstuffer', level='info', log_folder='/var/log/')
    logger.info("start application credstuffer")

    if args.subcommand == 'file':
        if args.path is not None:
            logger.info("process file")
            stuffer = Stuffing(filepath=args.path)
            stuffer.run()
        else:
            # currently not supported
            logger.info("process directory")
    else:
        logger.info("process database parameters")
        host = args.host
        port = args.port
        username = args.user
        password = args.password
        dbname = args.dbname
        dbparams = {'host': host, 'port': port, 'username': username, 'password': password, 'dbname': dbname}

        stuffer = Stuffing(**dbparams)
        stuffer.run()


if __name__ == '__main__':
    main()
