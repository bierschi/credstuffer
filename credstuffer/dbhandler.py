import logging

from credstuffer.db import DBConnector, DBFetcher, DBInserter
from credstuffer.exceptions import DBConnectorError


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

            if DBConnector.connect_psycopg(host=self.db_host, port=self.db_port, username=self.db_username,
                                           password=self.db_password, dbname=self.db_name, minConn=1, maxConn=39):

                # database instances
                self.dbfetcher = DBFetcher()
                self.dbinserter = DBInserter()

                # database schema structure
                self.dbstructure = '0123456789abcdefghijklmnopqrstuvwxyz'
                self.schema_list_default = list(self.dbstructure)
                self.schema_list_default.append('symbols')
                self.table_list_default = self.schema_list_default

                self.schema_list = None
                self.table_list = None
            else:
                self.logger.error("DBHandler could not connect to the databases")
                raise DBConnectorError("DBHandler could not connect to the databases")
        else:
            self.logger.error("DBHandler could not connect to the databases")
            raise DBConnectorError("DBHandler could not connect to the databases")

    def fetch_data(self, schema, table):
        """ fetch data from database table 'schema'.'table'

        :param schema: schema name
        :param table: table name

        :return: data from database table
        """
        sql = "select * from \"{}\".\"{}\"".format(schema, table)

        return self.dbfetcher.all(sql=sql)

