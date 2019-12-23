import logging
from credstuffer.db import DBConnector, DBFetcher, DBInserter


class DBHandler:
    """ Base class DBHandler to provide database actions to subclasses

    USAGE:
            dbhandler = DBHandler()

    """
    def __init__(self, **dbparams):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class DBHandler')
        print(dbparams)
        if ('host' and 'port' and 'username' and 'password' and 'dbname') in dbparams.keys():
            self.db_host = dbparams['host']
            self.db_port = dbparams['port']
            self.db_username = dbparams['username']
            self.db_password = dbparams['password']
            self.db_name = dbparams['dbname']
        else:
            self.logger.error("no database params provided!")

        DBConnector.connect_psycopg(host=self.db_host, port=self.db_port, username=self.db_username,
                                    password=self.db_password, dbname=self.db_name, minConn=1, maxConn=39)

        # database instances
        self.dbfetcher = DBFetcher()

