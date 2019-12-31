import unittest
from credstuffer import Proxy


class TestProxy(unittest.TestCase):

    def setUp(self) -> None:

        # set up Proxy instance
        self.proxy = Proxy(timeout_ms=50)

    def test_get(self):

        proxy = self.proxy.get()

        self.assertIsInstance(proxy, str, msg="proxy must be type of string")

    def test_load_proxies(self):

        proxy_list = self.proxy.load_proxies(timeout=50)

        self.assertIsInstance(proxy_list, list, msg="proxy list must be type of list")
        for proxy in proxy_list:
            self.assertIsInstance(proxy, str, msg="proxy must be type of string")

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
