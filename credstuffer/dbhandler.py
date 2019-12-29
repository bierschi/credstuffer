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

        if ('host' and 'port' and 'username' and 'password' and 'dbname') in dbparams.keys():
            self.db_host = dbparams['host']
            self.db_port = dbparams['port']
            self.db_username = dbparams['username']
            self.db_password = dbparams['password']
            self.db_name = dbparams['dbname']

            DBConnector.connect_psycopg(host=self.db_host, port=self.db_port, username=self.db_username,
                                        password=self.db_password, dbname=self.db_name, minConn=1, maxConn=39)

            # database instances
            self.dbfetcher = DBFetcher()
            self.dbinserter = DBInserter()

            # database schema structure
            self.dbstructure = '0123456789abcdefghijklmnopqrstuvwxyz'
            self.schema_list = list(self.dbstructure)
            self.schema_list.append('symbols')

        else:
            self.logger.error("no database params provided!")

    def fetch_data(self, schema, table):
        """

        :param schema:
        :param table:
        :return:
        """
        sql = "select * from \"{}\".\"{}\"".format(schema, table)

        return self.dbfetcher.all(sql=sql)

if __name__ == '__main__':
    pass
    #db = DBHandler(**dbparams)
    #db.fetch_data("a", "g")
