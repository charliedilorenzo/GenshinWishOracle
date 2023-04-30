import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genshinwishoracle.settings')
django.setup()
from django.test import TestCase
from .. import settings, database
from ..analytical import AnalyzeCharacter, AnalyzeWeapon, DataPoint, Statistic
from ..helpers import within_epsilon_or_greater


global schema_file, path
path = settings.BASE_DIR / "genshinwishoracle"
schema_file = path / "schema.sql"

class AnalyticalTestClass(TestCase):
    # normally bad practice but this is fine for using the lookup functions
    test_db = path / "tests" / "testing_analytical.sqlite3"
    analytical_weapon = AnalyzeWeapon(test_db)
    analytical_character = AnalyzeCharacter(test_db)
    # Weapon Analytical

    @classmethod
    def setUpTestData(cls):
        test_db = path / "tests" / "testing_analytical.sqlite3"
        database.reset_database(test_db)
        analytical_weapon = AnalyzeWeapon(db_file=test_db)
        analytical_character = AnalyzeCharacter(db_file=test_db)


    def setUp(self):
        pass

    def test_weapon_lookups_negative_pity(self):
        analytical_weapon = self.analytical_weapon
        pity = -1
        wish_num = 1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        self.assertEqual(lookup,-1)

    def test_weapon_lookups_above_hard_pity(self):
        analytical_weapon = self.analytical_weapon
        pity = analytical_weapon.hard_pity+1
        wish_num = 1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        self.assertEqual(lookup,-1)

    def test_weapon_lookups_negative_num_wish(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = -1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        self.assertEqual(lookup,-1)

    def test_weapon_lookups_above_max_wishes(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = analytical_weapon.max_wishes_required+1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        self.assertEqual(lookup,-1)

    def test_weapon_lookups_invalid_guaranteed(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = 1
        guaranteed = "False"
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        self.assertEqual(lookup,-1)

    def test_weapon_lookups_negative_fate_points(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = 1
        guaranteed = False
        fate_points = -1
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        self.assertEqual(lookup,-1)

    def test_weapon_lookups_above_max_fate_points(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = 1
        guaranteed = False
        fate_points = analytical_weapon.fate_points_required+1
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        self.assertEqual(lookup,-1)

    def test_weapon_lookups_are_invertible(self):
        # this also tests that all values are non-errored into a -1
        analytical_weapon = self.analytical_weapon
        max_pity = analytical_weapon.hard_pity
        max_wishes_required = analytical_weapon.max_wishes_required
        max_fate_points = analytical_weapon.fate_points_required

        for i in range(0, max_wishes_required):
            wish_num = i
            for j in range(0, max_pity):
                pity = j
                for k in range(0, 2):
                    for m in range(0, max_fate_points):
                        fate_points = m
                        if k == 0:
                            guaranteed = False
                        else:
                            guaranteed = True
                        lookup = analytical_weapon.lookup_num_generator(
                            wish_num, pity, guaranteed, fate_points)
                        reverse = analytical_weapon.lookup_num_to_setting(
                            lookup)
                        if not (wish_num == reverse[0] and pity == reverse[1] and guaranteed == reverse[2] and fate_points == reverse[3]):
                            self.assertTrue(False)
        self.assertTrue(True)

    # Character Analytical

    def test_character_lookups_negative_pity(self):
        analytical_character = self.analytical_character
        pity = -1
        wish_num = 1
        guaranteed = False
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        self.assertEqual(lookup,-1)

    def test_character_lookups_above_hard_pity(self):
        analytical_character = self.analytical_character
        pity = analytical_character.hard_pity+1
        wish_num = 1
        guaranteed = False
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        self.assertEqual(lookup,-1)

    def test_character_lookups_negative_num_wish(self):
        analytical_character = self.analytical_character
        pity = 0
        wish_num = -1
        guaranteed = False
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        self.assertEqual(lookup,-1)

    def test_character_lookups_above_max_wishes(self):
        analytical_character = self.analytical_character
        pity = 0
        wish_num = analytical_character.max_wishes_required+1
        guaranteed = False
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        self.assertEqual(lookup,-1)

    def test_character_lookups_invalid_guaranteed(self):
        analytical_character = self.analytical_character
        pity = 0
        wish_num = 1
        guaranteed = "False"
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        self.assertEqual(lookup,-1)

    def test_character_lookups_are_invertible(self):
        analytical_character = self.analytical_character
        max_pity = analytical_character.hard_pity
        max_wishes_required = analytical_character.max_wishes_required
        fate_points = 0
        for i in range(0, max_wishes_required):
            wish_num = i
            for j in range(0, max_pity):
                pity = j
                for k in range(0, 2):
                    if k == 0:
                        guaranteed = False
                    else:
                        guaranteed = True
                    lookup = analytical_character.lookup_num_generator(
                        wish_num, pity, guaranteed,fate_points)
                    reverse = analytical_character.lookup_num_to_setting(
                        lookup)
                    if not (wish_num == reverse[0] and pity == reverse[1] and guaranteed == reverse[2]):
                        self.assertTrue(False)
        self.assertTrue(True)

    def test_probabilities_all_around_one_character(self):
        analytical_character = self.analytical_character
        analytical_character.calculate_and_write_all_solutions()
        analytical_character.refresh_database_size()
        database_size = analytical_character.database_size
        if not analytical_character.database_is_full():
            self.assertTrue(False)
        
        max_pity = analytical_character.hard_pity
        max_wishes_required = analytical_character.max_wishes_required

        for i in range(0, max_wishes_required):
            wish_num = i
            for j in range(0, max_pity):
                pity = j
                for k in range(0, 2):
                    if k == 0:
                        guaranteed = False
                    else:
                        guaranteed = True
                    lookup = analytical_character.lookup_num_generator(wish_num, pity, guaranteed, 0)
                    result = analytical_character.hashtable[lookup]
                    self.assertAlmostEqual(1,sum(result))
                    # result = analytical_character.specific_solution(wish_num, pity, guaranteed, 0,0)
                    # self.assertAlmostEqual(1,sum(result.values()))
        self.assertTrue(True)

    def test_probabilities_all_around_one_weapon(self):
        analytical_weapon = self.analytical_weapon
        analytical_weapon.calculate_and_write_all_solutions()
        analytical_weapon.refresh_database_size()
        database_size = analytical_weapon.database_size
        if not analytical_weapon.database_is_full():
            self.assertTrue(False)

        max_pity = analytical_weapon.hard_pity
        max_wishes_required = analytical_weapon.max_wishes_required
        max_fate_points = analytical_weapon.fate_points_required

        for i in range(0, max_wishes_required):
            wish_num = i
            for j in range(0, max_pity):
                pity = j
                for k in range(0, 2):
                    for m in range(0, max_fate_points):
                        fate_points = m
                        if k == 0:
                            guaranteed = False
                        else:
                            guaranteed = True
                        # faster this way and should be equally accurate
                        lookup = analytical_weapon.lookup_num_generator(wish_num, pity, guaranteed, fate_points)
                        result = analytical_weapon.hashtable[lookup]
                        self.assertAlmostEqual(1,sum(result))
                        # result = analytical_weapon.specific_solution(wish_num, pity, guaranteed, fate_points,0)
                        # self.assertAlmostEqual(1,sum(result.values()))
        self.assertTrue(True)

    def test_create_data_points(self):
        labels = ["X", "C0","C1","C2","C3","C4","C5","C6"]
        values = [1,2,3,4,5,6,7,8]
        for i in range(0,len(labels)):
            datapoint = DataPoint(labels[i],values[i])
            self.assertEqual(datapoint.label, labels[i])
            self.assertEqual(datapoint.value, values[i])

    def test_create_statistic_character(self):
        values = [1,2,3,4,5,6,7,8]
        banner_type = "character"
        stat = Statistic(values, banner_type)
        expected_labels = ["X"]+["C{}".format(i) for i in range(0,7)]
        self.assertEqual(stat.labels, expected_labels)
        self.assertEqual(stat.banner_type, "Character")
    
    def test_create_statistic_weapon(self):
        values = [1,2,3,4,5,6]
        banner_type = "weapon"
        stat = Statistic(values, banner_type)
        expected_labels = ["X"]+["R{}".format(i) for i in range(1,6)]
        self.assertEqual(stat.labels, expected_labels)
        self.assertEqual(stat.banner_type, "Weapon")

    # python manage.py test genshinwishoracle.tests.test_analytical.AnalyticalTestClass.test_statistic_get_formatted_dictionary
    def test_statistic_get_formatted_dictionary(self):
        values = [1,2,3,4,5,6,7,8]
        banner_type = "character"
        stat = Statistic(values, banner_type)
        formatted = stat.get_formated_dictionary()
        expected =  {'X': '1.0000', 'C0': '2.0000', 'C1': '3.0000', 'C2': '4.0000', 'C3': '5.0000', 'C4': '6.0000', 'C5': '7.0000', 'C6': '8.0000'}
        self.assertEqual(expected,formatted)

    def test_statistic_get_data_points(self):
        values = [1,2,3,4,5,6,7,8]
        labels = ["X", "C0","C1","C2","C3","C4","C5","C6"]
        banner_type = "character"
        stat = Statistic(values, banner_type)
        datapoints = stat.get_data_points()
        for data in datapoints:
            self.assertEqual(data.label, stat.label)
            self.assertEqual(data.value, stat.values)
            self.assertEqual(data.datapoints, )


    def test_analyze_take_solution_from_database(self):
        # TODO
        pass
    
    def test_NEW(self):
        # for val in self.hashtable: incomplete_lookups.discard(val)
        # TODO
        pass

    def test_probability_on_copies_to_num_wishes(self):
        # for val in self.hashtable: incomplete_lookups.discard(val)
        # TODO
        pass
    
    def test_database_is_full_on_init_character(self):
        analytical_character_generate = AnalyzeCharacter(self.test_db)
        analytical_character = AnalyzeCharacter(self.test_db)


    def test_get_statistic_character_unformatted(self):
        result = self.analytical_character.get_statistic(0,0,0,0,0,False)
        expected_results = [1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        expected_results = Statistic(expected_results,"character",False)
        
        self.assertEqual(result.values, expected_results.values)
        self.assertEqual(result.labels, expected_results.labels)
        self.assertEqual(result.datapoints, expected_results.datapoints)
        self.assertEqual(result.banner_type, expected_results.banner_type)
        self.assertEqual(result.place_values, expected_results.place_values)

    def test_refresh_database_size_character(self):
        # TODO
        pass

    def test_db_file_doesnt_exist_character(self):
        os.remove(self.test_db)
        analytical_character_generate = AnalyzeCharacter(self.test_db)

    def test_specific_solution_database_full_character(self):
        analytical_character_generate = AnalyzeCharacter(self.test_db)
        analytical_character = AnalyzeCharacter(self.test_db)
        result = analytical_character.specific_solution(1,0,0,0,0)
        expected_results = [0.997, 0.003,0.0,0.0,0.0,0.0,0.0,0.0]
        self.assertEqual(result,expected_results)

    

    def test_database_is_full_on_init_weapon(self):
        analytical_weapon_generate = AnalyzeWeapon(self.test_db)
        analytical_weapon = AnalyzeWeapon(self.test_db)

    def test_get_statistic_weapon_unformatted(self):
        result = self.analytical_weapon.get_statistic(0,0,0,0,0,False)
        expected_results = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        expected_results = Statistic(expected_results,"weapon",False)
        self.assertEqual(result.values, expected_results.values)
        self.assertEqual(result.labels, expected_results.labels)
        self.assertEqual(result.datapoints, expected_results.datapoints)
        self.assertEqual(result.banner_type, expected_results.banner_type)
        self.assertEqual(result.place_values, expected_results.place_values)

    def test_refresh_database_size_weapon(self):
        # TODO
        pass

    def test_db_file_doesnt_exist_weapon(self):
        os.remove(self.test_db)
        analytical_weapon_generate = AnalyzeWeapon(self.test_db)

    def test_specific_solution_database_full_weapon(self):
        analytical_weapon_generate = AnalyzeWeapon(self.test_db)
        analytical_weapon = AnalyzeWeapon(self.test_db)
        result = analytical_weapon.specific_solution(1,0,0,0,0)
        expected_results = [1 - (.006*(.375+.25)), (.006*(.375)),0.0,0.0,0.0,0.0,0.0,0.0]
        for i in range(0,len(result)):
            self.assertAlmostEqual(result[i],expected_results[i],)