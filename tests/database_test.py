import pytest
import sqlite3
from mainstuff import database
import os


class TestClass:
    cwd = os.getcwd()
    main_dir = cwd.replace("\\testing", "")
    test_db_name = main_dir+"\\testing\\testing.db"
    database.reset_database(test_db_name)

    def get_test_db_name(self):
        return self.test_db_name

    def get_test_db_conn(self):
        conn = sqlite3.connect(self.get_test_db_name())
        return conn

    def test_reset_database_empty_end_result(self):
        database.reset_database(self.get_test_db_name())
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        for table in tables:
            current_table = database.table_data_to_hashtable(table, conn)
            assert current_table == {}

    def test_create_tables_tables_exist(self):
        conn = self.get_test_db_conn
        database.create_data_tables(conn)
        cur = conn.cursor()
        tables = []
        for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            tables.append(row)
        assert len(tables) > 0

    def test_update_data_in_table_non_error(self):
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        example_table = 'character_banners'
        if example_table not in tables:
            assert 0
            return 0
        data = [(1, 0, 0, 0, 0, 0, 0, 0)]
        database.update_data_in_table(data, example_table, conn)
        expected = {1: [0, 0, 0, 0, 0, 0, 0]}
        hashtable = database.table_data_to_hashtable(example_table, conn)
        assert hashtable == expected

    def test_table_to_hashtable(self):
        conn = self.get_test_db_conn

        pass

    def test_create_tables_tables_are_empty(self):
        conn = self.get_test_db_conn
        database.create_data_tables(conn)
        cur = conn.cursor()
        tables = []
        for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
            tables.append(row)
        assert len(tables) > 0

    def test_one(self):
        # assert "h" in x
        pass
