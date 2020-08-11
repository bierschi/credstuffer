import logging
import requests
from random import choice, seed


class Proxy:
    """ class Proxy to provide multiple proxies to request the accounts

    USAGE:
            proxy = Proxy(timeout_ms=50)
            proxy.get()

    """
    def __init__(self, timeout_ms=50):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Proxy')

        self.timeout_ms = timeout_ms
        self.timeout_counter = 1
        self.seed = seed(1)
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.session = requests.Session()
        self.proxies = self.load_proxies(timeout=self.calc_timeout(timeout_ms=self.timeout_ms))
        self.logger.info("Loaded {} proxies with timeout of {} ms".format(len(self.proxies), self.timeout_ms))

    def __del__(self):
        """destructor"""

        self.session.close()

    def get(self):
        """ returns a proxy

        :return: one proxy as ip:port
        """

        if len(self.proxies) > 0:
            proxy = choice(self.proxies)
            self.proxies.remove(proxy)
            return proxy
        else:
            timeout_ms = self.calc_timeout(timeout_ms=self.timeout_ms)
            self.proxies = self.load_proxies(timeout_ms)
            self.logger.info("Loaded {} proxies with timeout of {} ms".format(len(self.proxies), timeout_ms))
            return self.get()

    def load_proxies(self, timeout):
        """ loads proxies with given timeout from proxyscrape

        :return: list of proxies as ip:port
        """
        proxyscrape_url = self.__build_proxyscrape_url(timeout=timeout)
        response = self.__request(url=proxyscrape_url)

        return list(filter(None, response.content.decode('utf-8').split('\r\n')))

    def calc_timeout(self, timeout_ms):
        """ raises the timeout to fetch more proxies from webpage

        :param timeout_ms: timeout in ms
        :return: timeout_ms
        """
        timeout_ms = timeout_ms * self.timeout_counter
        self.timeout_counter += 1

        return timeout_ms

    def __request(self, url):
        """ requests the proxyscrape url

        :return: request response
        """
        return self.session.get(url=url, headers=self.headers)

    def __build_proxyscrape_url(self, proxytype='all', timeout=1000, ssl='yes', anonymity='all', country='all'):
        """ defines the proxyscrape url

        :param proxytype: type of proxy
        :param timeout: timeout for proxies
        :param ssl: ssl proxy
        :param anonymity: anonymity proxy
        :param country: country for proxy
        :return: url string
        """
        if proxytype not in ('http', 'socks4', 'socks5', 'all'):
            raise ValueError('proxytype {} is not a valid value'.format(proxytype))

        if timeout <= 0:
            raise ValueError('timeout must be an integer greater than 0')

        if ssl not in ('yes', 'no', 'all'):
            raise ValueError('ssl is not valid')

        if anonymity not in ('elite', 'anonymous', 'transparent', 'all'):
            raise ValueError('anonymity is not valid')

        if len(country) != 2 and country != 'all':
            raise ValueError('country is not valid')

        url = 'https://api.proxyscrape.com?request=getproxies' + \
              '&proxytype=%s' % proxytype + \
              '&timeout=%s'   % timeout + \
              '&ssl=%s'       % ssl + \
              '&anonymity=%s' % anonymity + \
              '&country=%s'   % country

        return url

