import argparse
from credstuffer.utils.logger import Logger


def main():

    # set up logger instance
    logger = Logger(name='credstuffer', level='info', log_folder='/var/log/')
    logger.info("start application credstuffer")


if __name__ == '__main__':
    main()
