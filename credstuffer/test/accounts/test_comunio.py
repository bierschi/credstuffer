import unittest
from credstuffer.accounts import Comunio


class TestComunio(unittest.TestCase):

    def setUp(self) -> None:

        # set up Comunio instance
        self.comunio = Comunio(max_requests=10)

    def test_set_usernames(self):

        self.comunio.set_usernames(usernames=['abc', 'abcd', 'abcde'])
        usernames = self.comunio.usernames

        self.assertIsInstance(usernames, list, msg="usernames must be type of list")
        self.assertEqual(len(usernames), 3, msg="wrong length of usernames")

    def test_login(self):
        pass

    def test_set_proxy(self):

        self.comunio.set_proxy(proxy={'http': '188.166.83.13:3128'})
        proxy = self.comunio.session.proxies

        self.assertIsInstance(proxy, dict, msg="proxy must be type of dictionary")
        self.assertEqual(proxy['http'], '188.166.83.13:3128', msg="proxy not set")

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
