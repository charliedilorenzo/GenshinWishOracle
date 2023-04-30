import sqlite3
import os
from pathlib import Path
from django.test import TestCase
from .. import settings, database, analytical

global schema_file, path
path = settings.BASE_DIR / "genshinwishoracle"
schema_file = path / "schema.sql"

class DatebaseTestCase(TestCase):
    cwd = os.getcwd()
    main_dir = settings.BASE_DIR 
    main_dir = main_dir / "genshinwishoracle"
    test_db_name = main_dir / "tests/testing.db"
    # schema_filepath = cwd.replace("\\tests", "")
    schema_filepath = main_dir / "schema.sql"
    test_db = path / "tests" / "testing_analytical.sqlite3"

    @classmethod
    def setUpTestData(cls):
        test_db = path / "tests" / "testing_analytical.sqlite3"
        if database.check_db:
            os.remove(test_db)
        # else:
        #     raise Exception("DATABASE NOT FOUND IN SETUP")
        database.init_db(test_db)

    def get_test_db_name(self):
        path = settings.BASE_DIR / "genshinwishoracle"
        return path / "tests" / "testing_analytical.sqlite3"

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

    def reset_database(self):
        database.reset_database(self.get_test_db_name())

    def test_init_file_exists(self):
        # os.remove(self.test_db)
        database.reset_database(self.test_db)
        # TODO make it so that this actually clears the tables themselves
        # self.assertTrue(database.check_db(self.test_db))
        database.init_db(self.test_db)
        self.assertTrue(database.check_db(self.test_db))
        conn = self.get_test_db_conn()
        expected_tables = ['analytical_solutions_character',
                           'analytical_solutions_weapon']
        tables = database.get_tables(conn)
        self.assertEqual(expected_tables, tables)


    def test_reset_database_empty_end_result(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        tables = database.get_tables(conn)
        for table in tables:
            current_table = database.table_data_to_hashtable(table, conn)
            assert current_table == {}
        self.reset_database()

    def test_reset_database_clears_data(self):
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
    
    def test_check_tables_expected_tables(self):
        expected_tables = ['analytical_solutions_character',
                           'analytical_solutions_weapon']
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

    def test_get_primary_keys(self):
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
                           'analytical_solutions_weapon']
        self.reset_database()
        conn = self.get_test_db_conn()
        database.create_data_tables(conn)
        tables = database.get_tables(conn)
        assert len(tables) > 0
        assert tables == expected_tables
        self.reset_database()

    def test_create_tables_tables_exist(self):
        expected_tables = ['analytical_solutions_character',
                           'analytical_solutions_weapon']
        self.reset_database()

        special_test_db = self.main_dir / "tests/tablesexisttest.db"
        if database.check_db(special_test_db):
            os.remove(special_test_db)
        Path(special_test_db).touch()

        conn = self.get_test_db_conn()
        database.create_data_tables(conn)
        tables = database.get_tables(conn)
        assert len(tables) > 0
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

        database.create_data_tables(conn)
        # is it still there
        for table in tables:
            current_table = database.table_data_to_hashtable(table, conn)
            assert current_table != {}

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

    def test_count_entries_in_table(self):
        analytical_weapon = analytical.AnalyzeWeapon(db_file=self.test_db)
        analytical_character = analytical.AnalyzeCharacter(db_file=self.test_db)
        # analytical_character.
        with self.get_test_db_conn() as conn:
            database.count_entries_in_table(analytical_character.tablename, conn)
            database.count_entries_in_table(analytical_weapon.tablename, conn)

    def test_get_entry_by_primary_key_analytical(self):
        self.reset_database()
        conn = self.get_test_db_conn()
        analytical_weapon = analytical.AnalyzeWeapon(db_file=self.test_db)
        table_name = "analytical_solutions_weapon"
        lookup = 0
        entry = database.get_entry_by_primary_key_analytical(table_name, conn, lookup)
        expected_result = [1.0,0.0,0.0,0.0,0.0,0.0]
        entry = list(entry)
        self.assertEqual(entry,expected_result)
