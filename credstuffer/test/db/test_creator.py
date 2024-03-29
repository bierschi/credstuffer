import unittest
from credstuffer.db.inserter import DBInserter
from credstuffer.db.creator import DBCreator, Table, Column
from credstuffer.db.connector import DBConnector


class TestDBCreator(unittest.TestCase):

    def setUp(self) -> None:

        # set up DBConnector instance
        DBConnector().connect_psycopg(host="192.168.178.200", port=5432, username="postgres", password="postgres", dbname="postgres")
        self.inserter = DBInserter()
        self.creator = DBCreator()
        self.creator.build(obj=Table("test", Column(name="id", type="bigint"),
                                             Column(name="username", type="text")))

    def test_database(self):
        pass

    def test_schema(self):
        pass

    def test_table(self):

        self.table_str = Table("test", Column(name="id", type="bigint"),
                                       Column(name="id2", type="text")).__repr__()

        self.assertIsInstance(self.table_str, str, msg="table creation must be type of string")
        self.assertEqual(self.table_str, "create table if not exists test (id bigint , id2 text )", msg="table creation string is faulty")

    def test_column(self):

        self.colum_str = Column(name="id", type="bigint").__repr__()

        self.assertIsInstance(self.colum_str, str, msg="colum creation must be type of string")
        self.assertEqual(self.colum_str, "id bigint ", msg="colum creation string is faulty")

    def tearDown(self) -> None:

        sql = "delete from test"
        self.inserter.sql(sql=sql)


if __name__ == '__main__':
    unittest.main()
