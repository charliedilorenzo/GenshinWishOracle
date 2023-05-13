import sqlite3
import os
from pathlib import Path
from django.test import TestCase
from .. import settings, analytical
from ..database import *

global schema_file, path
path = settings.BASE_DIR / "genshinwishoracle"
schema_file = path / "schema.sql"

class DatebaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_db = path / "tests" / "testing_database.sqlite3"
        cls.test_db = test_db
        if check_db(test_db):
            os.remove(test_db)
        init_db(test_db)

        cls.analytical_weapon = analytical.AnalyzeWeapon(db_file=test_db)
        with sqlite3.connect(test_db) as conn:
            clear_table(cls.analytical_weapon.tablename, conn)
        cls.analytical_character = analytical.AnalyzeCharacter(db_file=test_db)
        with sqlite3.connect(test_db) as conn:
            clear_table(cls.analytical_character.tablename, conn)
        cls.data = {'analytical_solutions_character': [tuple([float(i) for i in range(0, 9)])], 'analytical_solutions_weapon': [tuple([i for i in range(0, 7)])]}

        main_dir = settings.BASE_DIR / "genshinwishoracle"
        cls.main_dir = main_dir
        schema_filepath = main_dir / "schema.sql"

    def setUp(self):
        self.reset_database()

    def get_test_db_name(self):
        path = settings.BASE_DIR / "genshinwishoracle"
        return path / "tests" / "testing_database.sqlite3"

    def get_test_db_conn(self):
        conn = sqlite3.connect(self.get_test_db_name())
        return conn

    def add_example_data_to_all_tables(self):
        with sqlite3.connect(self.get_test_db_name()) as conn:
            update_data_in_table(
                self.data['analytical_solutions_character'], 'analytical_solutions_character', conn)
        with sqlite3.connect(self.get_test_db_name()) as conn:
            update_data_in_table(
                self.data['analytical_solutions_weapon'], 'analytical_solutions_weapon', conn)

    def reset_database(self):
        reset_database(self.get_test_db_name())

    def test_greaterthan(self):
        # TODO GET RID OF THIS
        greater = 1
        lesser = .5
        self.assertGreaterEqual(greater, lesser)

    def test_init_file_exists(self):
        # os.remove(self.test_db)
        # TODO make it so that this actually clears the tables themselves
        init_db(self.test_db)
        self.assertTrue(check_db(self.test_db))
        expected_tables = ['analytical_solutions_character',
                            'analytical_solutions_weapon']
        with sqlite3.connect(self.get_test_db_name()) as conn:
            tables = get_tables(conn)
        self.assertEqual(expected_tables, tables)


    def test_reset_database_empty_end_result(self):
        with sqlite3.connect(self.get_test_db_name()) as conn:
            tables = get_tables(conn)
            for table in tables:
                current_table = table_data_to_hashtable(table, conn)
                assert current_table == {}

    def test_reset_database_clears_data(self):
        with sqlite3.connect(self.get_test_db_name()) as conn:
            tables = get_tables(conn)

        # add the data
        self.add_example_data_to_all_tables()
        with sqlite3.connect(self.get_test_db_name()) as conn:
            for table in tables:
                current_table = table_data_to_hashtable(table, conn)
                self.assertNotEqual(current_table, {})
            self.reset_database()
            for table in tables:
                current_table = table_data_to_hashtable(table, conn)
                self.assertEqual(current_table, {})
    
    def test_check_tables_expected_tables(self):
        expected_tables = ['analytical_solutions_character',
                           'analytical_solutions_weapon']
        with sqlite3.connect(self.get_test_db_name()) as conn:
            for table in expected_tables:
                check = check_table(table, conn)
                assert check == True

    def test_check_tables_unexpected_table(self):
        unexpected_table = 'this_table_is_so_totally_unexpected_bro'
        with sqlite3.connect(self.get_test_db_name()) as conn:
            check = check_table(unexpected_table, conn)
        self.assertFalse(check)

    def test_get_primary_keys(self):
        self.add_example_data_to_all_tables()
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
        with sqlite3.connect(self.get_test_db_name()) as conn:
            update_data_in_table(
                data, table, conn)
        with sqlite3.connect(self.get_test_db_name()) as conn:
            keys = get_primary_keys(table, conn)
        assert keys == expected

    def test_get_tables(self):
        expected_tables = ['analytical_solutions_character',
                           'analytical_solutions_weapon']
        self.reset_database()
        with sqlite3.connect(self.get_test_db_name()) as conn:
            create_data_tables(conn)
            tables = get_tables(conn)
        self.assertTrue(len(tables) > 0)
        self.assertEqual(tables, expected_tables)

    def test_create_tables_tables_exist(self):
        expected_tables = ['analytical_solutions_character',
                           'analytical_solutions_weapon']
        self.reset_database()
        if check_db(self.test_db):
            os.remove(self.test_db)
        Path(self.test_db).touch()
        with sqlite3.connect(self.get_test_db_name()) as conn:
            create_data_tables(conn)
        with sqlite3.connect(self.get_test_db_name()) as conn:
            tables = get_tables(conn)
        assert len(tables) > 0
        assert tables == expected_tables

    def test_create_tables_on_database_doesnt_clear_existing_data(self):
        self.add_example_data_to_all_tables()
        with sqlite3.connect(self.get_test_db_name()) as conn:
            tables = get_tables(conn)
        # added data properly
        tables_data = []
        with sqlite3.connect(self.get_test_db_name()) as conn:
            for table in tables:
                expected_table = {int(self.data[table][0][0]): list(self.data[table][0][1:len(self.data[table][0])])}
                current_table = table_data_to_hashtable(table, conn)
                tables_data.append(current_table)
                self.assertEqual(expected_table,current_table)
        
        with sqlite3.connect(self.get_test_db_name()) as conn:
            create_data_tables(conn)
        # is it still there
        with sqlite3.connect(self.get_test_db_name()) as conn:
            for i in range(0,len(tables)):
                current_table = table_data_to_hashtable(tables[i], conn)
                self.assertEqual(tables_data[i],current_table)

        self.reset_database()

    def test_update_data_in_table_analytical_character(self):
        with sqlite3.connect(self.get_test_db_name()) as conn:
            tables = get_tables(conn)
        example_table = 'analytical_solutions_character'
        if example_table not in tables:
            self.assertTrue(False)

        # add the data
        data = [tuple(i for i in range(0, 9))]
        expected = {0: [i for i in range(1, 9)]}
        with sqlite3.connect(self.get_test_db_name()) as conn:
            update_data_in_table(data, example_table, conn)
            hashtable = table_data_to_hashtable(example_table, conn)
        self.assertEqual(hashtable,expected)

    def test_update_data_in_table_analytical_weapon(self):
        with sqlite3.connect(self.get_test_db_name()) as conn:
            tables = get_tables(conn)
        example_table = 'analytical_solutions_weapon'
        if example_table not in tables:
            self.assertTrue(False)
        data = [tuple(i for i in range(0, 7))]
        expected = {0: [i for i in range(1, 7)]}
        with sqlite3.connect(self.get_test_db_name()) as conn:
            update_data_in_table(data, example_table, conn)
            hashtable = table_data_to_hashtable(example_table, conn)
        self.assertEqual(hashtable,expected)

    def test_update_data_in_table_replacing_one_item_only(self):
        with sqlite3.connect(self.get_test_db_name()) as conn:
            tables = get_tables(conn)
        example_table = 'analytical_solutions_character'
        if example_table not in tables:
            self.assertTrue(False)

        # use it add the data
        data = [tuple(i for i in range(0, 9))]
        expected = {0: [i for i in range(1, 9)]}
        with sqlite3.connect(self.get_test_db_name()) as conn:
            update_data_in_table(data, example_table, conn)
            hashtable = table_data_to_hashtable(example_table, conn)
        self.assertEqual(hashtable,expected)

        # also to change it
        data = [0] + [i for i in range(8, 0, -1)]
        data = [tuple(data)]
        expected = {0: [i for i in range(8, 0, -1)]}
        with sqlite3.connect(self.get_test_db_name()) as conn:
            update_data_in_table(data, example_table, conn)
            hashtable = table_data_to_hashtable(example_table, conn)
        self.assertEqual(hashtable,expected)

    def test_update_data_in_table_replacing_one_item_add_one(self):
        with sqlite3.connect(self.get_test_db_name()) as conn:
            tables = get_tables(conn)
        example_table = 'analytical_solutions_character'
        if example_table not in tables:
            self.assertTrue(False)

        # use it add the data
        data = [tuple(i for i in range(0, 9))]
        expected = {0: [i for i in range(1, 9)]}
        with sqlite3.connect(self.get_test_db_name()) as conn:
            update_data_in_table(data, example_table, conn)
            hashtable = table_data_to_hashtable(example_table, conn)
        self.assertEqual(hashtable,expected)

        # replace current data with identical and add a new one
        data += [tuple([i for i in range(9, 0, -1)])]
        expected = {9: [i for i in range(
            8, 0, -1)], 0: [i for i in range(1, 9)]}
        with sqlite3.connect(self.get_test_db_name()) as conn:
            update_data_in_table(data, example_table, conn)
            hashtable = table_data_to_hashtable(example_table, conn)
        self.assertEqual(hashtable,expected)

    def test_count_entries_in_table(self):
        analytical_character = self.analytical_character
        analytical_weapon = self.analytical_weapon
        with sqlite3.connect(self.get_test_db_name()) as conn:
            count_entries_in_table(analytical_character.tablename, conn)
            count_entries_in_table(analytical_weapon.tablename, conn)
        # TODO THIS NEEDS AN ACTUAL TEST

    def test_get_entry_by_primary_key_analytical(self):
        analytical_weapon = self.analytical_weapon
        lookup = 1
        analytical_weapon.calculate_and_write_all_solutions()
        with sqlite3.connect(self.get_test_db_name()) as conn:
            entry = get_entry_by_primary_key_analytical(analytical_weapon.tablename, conn, lookup)
        expected_result = [1.0-(.375*0.006),(.375*0.006),0.0,0.0,0.0,0.0]
        entry = list(entry)
        for i in range(0,len(expected_result)):
            self.assertAlmostEqual(entry[i],expected_result[i])
    
    def test_get_default_db(self):
        database_file = get_default_db()
        end = str(database_file).split("/")[-1]
        # path
        self.assertTrue(end, "database.sqlite3")
        self.assertTrue(database_file, path / "database.sqlite3")

    def test_reset_database_doesnt_exist(self):
        # TODO ADD
        pass