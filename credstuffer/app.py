import argparse
from credstuffer.utils.logger import Logger
from credstuffer.logins.comunio import Comunio
from credstuffer.stuffing import Stuffing


def main():

    # arguments
    parser = argparse.ArgumentParser(description="")
    # database parameters
    parser.add_argument('--host',       type=str, help='hostname to connect to the database')
    parser.add_argument('--port',       type=str, help='port to connect to the database')
    parser.add_argument('--user',       type=str, help='user of the database')
    parser.add_argument('--password',   type=str, help='password from the user')
    parser.add_argument('--dbname',     type=str, help='database name')
    # breach compilation path
    parser.add_argument('--breachpath', type=str, help='path to the BreachCompilation collection folder')
    # password file path
    parser.add_argument('--filepath',   type=str, help='path to the password file')

    args = parser.parse_args()

    host = args.host
    port = args.port
    username = args.user
    password = args.password
    dbname = args.dbname
    dbparams = {'host': host, 'port': port, 'username': username, 'password': password, 'dbname': dbname}

    # set up logger instance
    logger = Logger(name='credstuffer', level='info', log_folder='/var/log/')
    logger.info("start application credstuffer")

    stuffer = Stuffing(**dbparams)
    #stuffer = Stuffing(filepath='/home/christian/projects/CredentialDatabase/Collections/rockyou.txt')
    stuffer.run()

if __name__ == '__main__':
    main()
