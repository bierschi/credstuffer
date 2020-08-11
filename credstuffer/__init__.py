__title__ = "credstuffer"
__version_info__ = ('1', '0', '13')
__version__ = ".".join(__version_info__)
__author__ = "Christian Bierschneider"
__email__ = "christian.bierschneider@web.de"
__license__ = "MIT"

import os
from credstuffer.account import Account
from credstuffer.user_account import UserAccount
from credstuffer.email_account import EmailAccount
from credstuffer.proxy import Proxy

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
