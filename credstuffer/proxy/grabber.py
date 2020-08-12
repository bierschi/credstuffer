import requests
import logging
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


class ProxyGrabber:
    """class ProxyGrabber to grab different kinds of proxies

    USAGE:
            grabber = ProxyGrabber()
            grabber.collect_proxies()
    """
    def __init__(self, timeout=1000, max_workers=8):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info("create class ProxyGrabber")

        # create request session
        self.timeout = timeout
        self.session = requests.Session()
        self.max_workers = max_workers
        self.proxy_types = {key: [] for key in ["http", "socks4", "socks5"]}

        self.proxyscrape_http_url   = self.__define_proxyscrape_url(proxytype='http', timeout=self.timeout)
        self.proxyscrape_socks4_url = self.__define_proxyscrape_url(proxytype='socks4', timeout=self.timeout)
        self.proxyscrape_socks5_url = self.__define_proxyscrape_url(proxytype='socks5', timeout=self.timeout)

        # used
        self.free_proxy_url  = 'https://free-proxy-list.net/'
        self.us_proxy_url    = 'https://us-proxy.org'
        self.socks_proxy_url = 'https://socks-proxy.net'
        self.ip_address_url  = 'https://www.ip-adress.com/proxy-list'
        self.proxy_daily_url = 'http://www.proxy-daily.com'

        self.anonymous_proxy_url = 'https://free-proxy-list.net/anonymous-proxy.html' # not
        self.ssl_proxy_url       = 'https://sslproxies.org' # not

        self.proxy_urls = [
            self.free_proxy_url,          # http
            self.us_proxy_url,            # http
            self.ip_address_url,          # http
            self.socks_proxy_url,         # socks4
            self.proxy_daily_url,         # http, socks4, socks5
            self.proxyscrape_http_url,    # http
            self.proxyscrape_socks4_url,  # socks4
            self.proxyscrape_socks5_url,  # socks5
        ]

    def collect_proxies(self, proxytype='all'):
        """ collects all proxies from url resources

        :param proxytype: type of proxies
        :return: proxy dict as ip:port string
        """
        self.logger.info("collecting proxies ...")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {executor.submit(self.__load_url, url, 5): url for url in self.proxy_urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    resp = future.result()
                    if (url in self.ip_address_url) and (proxytype in ('all', 'http')):
                        proxies = self.__parse_ipadress(response=resp)
                        self.proxy_types['http'].extend(proxies)
                    elif url in self.proxy_daily_url:
                        http, socks4, socks5 = self.__parse_proxy_daily(response=resp)
                        if proxytype == 'http':
                            self.proxy_types['http'].extend(http)
                        elif proxytype == 'socks4':
                            self.proxy_types['socks4'].extend(socks4)
                        elif proxytype == 'socks5':
                            self.proxy_types['socks5'].extend(socks5)
                        else:
                            self.proxy_types['http'].extend(http)
                            self.proxy_types['socks4'].extend(socks4)
                            self.proxy_types['socks5'].extend(socks5)
                    elif (url in (self.free_proxy_url, self.us_proxy_url)) and (proxytype in ('all', 'http')):
                        proxies = self.__parse_free_proxy(response=resp)
                        self.proxy_types['http'].extend(proxies)
                    elif (url in self.socks_proxy_url) and (proxytype in ('all', 'socks4')):
                        proxies = self.__parse_free_proxy(response=resp)
                        self.proxy_types['socks4'].extend(proxies)
                    elif (url in self.proxyscrape_http_url) and (proxytype in ('all', 'http')):
                        proxies = self.__parse_proxyscrape(response=resp)
                        self.proxy_types['http'].extend(proxies)
                    elif (url in self.proxyscrape_socks4_url) and (proxytype in ('all', 'socks4')):
                        proxies = self.__parse_proxyscrape(response=resp)
                        self.proxy_types['socks4'].extend(proxies)
                    elif (url in self.proxyscrape_socks5_url) and (proxytype in ('all', 'socks5')):
                        proxies = self.__parse_proxyscrape(response=resp)
                        self.proxy_types['socks5'].extend(proxies)
                except Exception as e:
                    self.logger.error(e)

        return self.proxy_types

    def __load_url(self, url, timeout=5):
        """ loads given url resource

        :param url: url string
        :param timeout: timeout
        :return: request response
        """
        return self.session.get(url=url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=timeout)

    def __define_proxyscrape_url(self, proxytype='all', timeout=1000, ssl='all', anonymity='all', country='all'):
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

### parser ####

    def __parse_free_proxy(self, response):
        """parses response from free-proxy-list.net

        :param url: string, url
        :return: list, list of proxies as ip:port
        """
        soup = BeautifulSoup(response.text, "html.parser")
        proxy_list = list()

        for items in soup.select("tbody tr"):
            proxy = ':'.join([item.text for item in items.select("td")[:2]])
            if ('-' in proxy) or (not proxy) or (':' not in proxy) or ('.' not in proxy):
                pass
            else:
                proxy_list.append(proxy)

        return proxy_list

    def __parse_ipadress(self, response):
        """parses response from ip-adress.com

        :return: list, ip:port as a string
        """

        soup = BeautifulSoup(response.text, "html.parser")
        parser = soup.find('tbody').find_all('tr')
        proxy_list = list()

        for elem in parser:
            elem = elem.get_text().split()[:2]
            if elem[1] != 'transparent':
                if ('-' in elem[0]) or (not elem[0]) or (':' not in elem[0]) or ('.' not in elem[0]):
                    pass
                else:
                    proxy_list.append(elem[0])

        return proxy_list

    def __parse_proxy_daily(self, response):
        """ parses response from proxy-daily.com

        :param response: response object
        :return: list, ip:port as a string
        """
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find('div', {'id': 'free-proxy-list'})
            all_content = content.find_all(class_="freeProxyStyle")
            http   = list(filter(None, all_content[0].contents[0].split('\n')))
            socks4 = list(filter(None, all_content[1].contents[0].split('\n')))
            socks5 = list(filter(None, all_content[2].contents[0].split('\n')))
            return http, socks4, socks5

        except (AttributeError, KeyError) as ex:
            self.logger.error(ex)

    def __parse_proxyscrape(self, response):
        """ parses response from proxyscrape.com

        :param response: response object
        :return: list, ip:port as a string
        """
        return list(filter(None, response.content.decode('utf-8').split('\r\n')))

