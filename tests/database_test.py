import pytest
import sqlite3
from mainstuff import database
import os
from pathlib import Path


class TestClass:
    cwd = os.getcwd()
    main_dir = cwd.replace("\\tests", "")
    main_dir = "C:\\Users\\carol\\Code\\Personal\\GenshinWishOracle"
    test_db_name = main_dir+"\\tests\\testing.db"
    schema_filepath = cwd.replace("\\tests", "")
    schema_filepath = schema_filepath + "\\mainstuff\\schema.sql"

    def get_test_db_name(self):
        return self.test_db_name

    def get_test_db_conn(self):
        conn = sqlite3.connect(self.get_test_db_name())
        return conn

    def add_example_data_to_all_tables(self):
        conn = self.get_test_db_conn()
        data = [tuple(i for i in range(0, 9))]
        database.update_data_in_table(
            data, 'analytical_solutions_character', conn)
        data = [tuple(i for i in range(0, 7))]
        database.update_data_in_table(
            data, 'analytical_solutions_weapon', conn)
        data = [("example banner character", "Baizhu", "Amber", "Kaeya", "Lisa")]
        database.update_data_in_table(
            data, 'character_banners', conn)
        data = [("example banner weapon", "Skyward Pride", "Wolf's Greatstone",
                 "The Bell", "Widsth", "Favonius Lance", "Stringless", "Lion's Roar")]
        database.update_data_in_table(
            data, 'weapon_banners', conn)

    def reset_database(self):
        database.reset_database(self.get_test_db_name())

    def test_reset_database_empty_end_result(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        for table in tables:
            current_table = database.table_data_to_hashtable(table, conn)
            assert current_table == {}
        self.reset_database()

    def test_reset_database_clears_data(self):
        # TODO
        self.reset_database()
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)

        # add the data
        self.add_example_data_to_all_tables()

        for table in tables:
            current_table = database.table_data_to_hashtable(table, conn)
            assert current_table != {}
        self.reset_database()
        for table in tables:
            current_table = database.table_data_to_hashtable(table, conn)
            assert current_table == {}
        self.reset_database()

    def test_get_primary_keys(self):
        # TODO
        self.reset_database()
        self.add_example_data_to_all_tables()
        conn = self.get_test_db_conn()
        table = 'analytical_solutions_character'

        data = []
        k = 1
        j = 1
        expected = [0]
        for i in range(0, 10):
            curr = k+j
            expected.append(curr)
            k = j
            j = curr
            curr = tuple([curr] + [i for i in range(1, 9)])
            data.append(curr)
        database.update_data_in_table(
            data, table, conn)

        keys = database.get_primary_keys(table, conn)
        assert keys == expected
        self.reset_database()

    def test_get_tables(self):
        expected_tables = ['analytical_solutions_character',
                           'analytical_solutions_weapon', 'character_banners', 'weapon_banners']
        self.reset_database()
        conn = self.get_test_db_conn()
        database.create_data_tables(self.schema_filepath, conn)
        tables = database.get_tables(conn)
        assert len(tables) > 0
        assert tables == expected_tables
        self.reset_database()

    def test_check_tables_expected_tables(self):
        expected_tables = ['analytical_solutions_character',
                           'analytical_solutions_weapon', 'character_banners', 'weapon_banners']
        self.reset_database()

        conn = self.get_test_db_conn()

        for table in expected_tables:
            check = database.check_table(table, conn)
            assert check == True
        self.reset_database()

    def test_check_tables_unexpected_table(self):
        self.reset_database()

        conn = self.get_test_db_conn()
        unexpected_table = 'this_table_is_so_totally_unexpected_bro'
        check = database.check_table(unexpected_table, conn)

    def test_create_tables_tables_exist(self):
        expected_tables = ['analytical_solutions_character',
                           'analytical_solutions_weapon', 'character_banners', 'weapon_banners']
        self.reset_database()

        special_test_db = self.main_dir + "\\tests\\tablesexisttest.db"
        if database.check_db(special_test_db):
            os.remove(special_test_db)
            print("here")
        Path(special_test_db).touch()

        conn = self.get_test_db_conn()
        database.create_data_tables(self.schema_filepath, conn)
        tables = database.get_tables(conn)
        assert len(tables) > 0
        print(tables)
        assert tables == expected_tables
        self.reset_database()

    def test_create_tables_on_database_doesnt_clear_existing_data(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        self.add_example_data_to_all_tables()
        tables = database.get_tables(conn)
        # added data properly
        for table in tables:
            current_table = database.table_data_to_hashtable(table, conn)
            assert current_table != {}

        database.create_data_tables(self.schema_filepath, conn)
        # is it still there
        for table in tables:
            current_table = database.table_data_to_hashtable(table, conn)
            assert current_table != {}

        self.reset_database()

    def test_init_db(self):
        # TODO
        pass

    def test_print_table(self, capsys):
        self.reset_database()
        conn = self.get_test_db_conn()
        table = 'analytical_solutions_character'

        data = []
        k = 1
        j = 1
        expected = ""
        for i in range(0, 10):
            curr = k+j
            k = j
            j = curr
            curr = tuple([curr] + [i for i in range(1, 9)])
            data.append(curr)
            curr_expected = [curr[0]] + \
                [float(curr[i]) for i in range(1, len(curr))]
            curr_expected = tuple(curr_expected)
            curr_expected = str(curr_expected)
            expected += curr_expected+"\n"

        database.update_data_in_table(
            data, table, conn)

        database.print_table(table, conn)
        out, err = capsys.readouterr()
        assert out == expected

        self.reset_database()

    def test_update_data_in_table_analytical_character(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        example_table = 'analytical_solutions_character'
        if example_table not in tables:
            assert 0

        # add the data
        data = [tuple(i for i in range(0, 9))]
        expected = {0: [i for i in range(1, 9)]}
        database.update_data_in_table(data, example_table, conn)
        hashtable = database.table_data_to_hashtable(example_table, conn)
        assert hashtable == expected

        self.reset_database()

    def test_update_data_in_table_analytical_weapon(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        example_table = 'analytical_solutions_weapon'
        if example_table not in tables:
            assert 0
        data = [tuple(i for i in range(0, 7))]
        database.update_data_in_table(data, example_table, conn)
        expected = {0: [i for i in range(1, 7)]}
        hashtable = database.table_data_to_hashtable(example_table, conn)
        assert hashtable == expected
        self.reset_database()

    def test_update_data_in_table_character_banners(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        example_table = 'character_banners'
        if example_table not in tables:
            assert 0
        data = [("example banner character", "Baizhu", "Amber", "Kaeya", "Lisa")]
        database.update_data_in_table(data, example_table, conn)
        expected = {"example banner character": [
            "Baizhu", "Amber", "Kaeya", "Lisa"]}
        hashtable = database.table_data_to_hashtable(example_table, conn)
        assert hashtable == expected
        self.reset_database()

    def test_update_data_in_table_weapon_banners(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        example_table = 'weapon_banners'
        if example_table not in tables:
            assert 0
        data = [("example banner weapon", "Skyward Pride", "Wolf's Greatstone",
                 "The Bell", "Widsth", "Favonius Lance", "Stringless", "Lion's Roar")]
        database.update_data_in_table(data, example_table, conn)
        expected = {"example banner weapon": [
            "Skyward Pride", "Wolf's Greatstone", "The Bell", "Widsth", "Favonius Lance", "Stringless", "Lion's Roar"]}
        hashtable = database.table_data_to_hashtable(example_table, conn)
        assert hashtable == expected
        self.reset_database()

    def test_update_data_in_table_replacing_one_item_only(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        example_table = 'analytical_solutions_character'
        if example_table not in tables:
            assert 0

        # use it add the data
        data = [tuple(i for i in range(0, 9))]
        expected = {0: [i for i in range(1, 9)]}
        database.update_data_in_table(data, example_table, conn)
        hashtable = database.table_data_to_hashtable(example_table, conn)
        assert hashtable == expected

        # also to change it
        data = [0] + [i for i in range(8, 0, -1)]
        data = [tuple(data)]
        expected = {0: [i for i in range(8, 0, -1)]}
        database.update_data_in_table(data, example_table, conn)
        hashtable = database.table_data_to_hashtable(example_table, conn)
        assert hashtable == expected

        self.reset_database()

    def test_update_data_in_table_replacing_one_item_add_one(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        example_table = 'analytical_solutions_character'
        if example_table not in tables:
            assert 0

        # use it add the data
        data = [tuple(i for i in range(0, 9))]
        expected = {0: [i for i in range(1, 9)]}
        database.update_data_in_table(data, example_table, conn)
        hashtable = database.table_data_to_hashtable(example_table, conn)
        assert hashtable == expected

        # replace current data with identical and add a new one
        data += [tuple([i for i in range(9, 0, -1)])]
        expected = {9: [i for i in range(
            8, 0, -1)], 0: [i for i in range(1, 9)]}
        database.update_data_in_table(data, example_table, conn)
        hashtable = database.table_data_to_hashtable(example_table, conn)
        assert hashtable == expected

        self.reset_database()

    def test_table_to_hashtable(self):
        # TODO
        self.reset_database()
        conn = self.get_test_db_conn
        self.reset_database()
        pass
