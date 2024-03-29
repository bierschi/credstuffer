import unittest
from credstuffer.db.fetcher import DBFetcher
from credstuffer.db.inserter import DBInserter
from credstuffer.db.creator import DBCreator, Table, Column
from credstuffer.db.connector import DBConnector


class TestDBFetcher(unittest.TestCase):

    def setUp(self) -> None:

        # set up DBConnector instance
        DBConnector().connect_psycopg(host="192.168.178.200", port=5432, username="postgres", password="postgres", dbname="postgres")
        self.fetcher = DBFetcher()
        self.inserter = DBInserter()
        self.creator = DBCreator()
        self.creator.build(obj=Table("test", Column(name="id", type="bigint"),
                                             Column(name="username", type="text")))

        sql = "insert into test (id, username) values (%s, %s)"
        self.inserter.many_rows(sql=sql, datas=[(0, "abc"), (1, "def"), (2, "ghi")])

    def test_one(self):

        sql = "select * from test"
        one_row = self.fetcher.one(sql=sql)

        self.assertIsInstance(one_row, tuple, msg="one row must be of type tuple")
        self.assertEqual(one_row[0], 0, msg="first element in one_row must be 0")
        self.assertEqual(one_row[1], 'abc', msg="second element in one_row must be 'abc'")

    def test_many(self):

        sql = "select * from test"
        rows = self.fetcher.many(sql=sql, size=2)

        self.assertIsInstance(rows, list, msg="rows must be of type tuple")
        self.assertEqual(len(rows), 2, msg="rows must be of length 2")

    def test_all(self):

        sql = "select * from test"
        all = self.fetcher.all(sql=sql)

        self.assertIsInstance(all, list, msg="rows must be of type tuple")
        self.assertEqual(len(all), 3, msg="rows must be of length 2")

    def tearDown(self) -> None:

        sql = "delete from test"
        self.inserter.sql(sql=sql)


if __name__ == '__main__':
    unittest.main()
