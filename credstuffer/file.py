import logging


class File:

    def __init__(self, path):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class File')

        self.path = path
    pass
