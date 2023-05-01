import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genshinwishoracle.settings')
django.setup()
from django.test import TestCase
from .. import settings, database
from ..analytical import *
from ..helpers import within_epsilon_or_greater


global schema_file, path
path = settings.BASE_DIR / "genshinwishoracle"
schema_file = path / "schema.sql"

class AnalyticalTestClass(TestCase):
    test_db = path / "tests" / "testing_analytical.sqlite3"

    @classmethod
    def setUpTestData(cls):
        test_db = path / "tests" / "testing_analytical.sqlite3"
        database.reset_database(test_db)
        cls.analytical_weapon = AnalyzeWeapon(db_file=test_db)
        cls.analytical_character = AnalyzeCharacter(db_file=test_db)

    def setUp(self):
        analytical_character =  self.analytical_character
        analytical_character.refresh_database_size()
        if not analytical_character.database_is_full():
            analytical_character.calculate_and_write_all_solutions()

        analytical_weapon =  self.analytical_weapon
        analytical_weapon.refresh_database_size()
        if not analytical_weapon.database_is_full():
            analytical_weapon.calculate_and_write_all_solutions()


    def test_db_file_doesnt_exist_character(self):
        os.remove(self.test_db)
        analytical_character_generate = AnalyzeCharacter(self.test_db)
    
    def test_db_file_doesnt_exist_weapon(self):
        os.remove(self.test_db)
        analytical_weapon_generate = AnalyzeWeapon(self.test_db)
    
    def test_refresh_database_size_db_doesnt_exist(self):
        os.remove(self.test_db)
        analytical_character = self.analytical_weapon
        analytical_weapon = self.analytical_character
        analytical_character.refresh_database_size()
        analytical_weapon.refresh_database_size()
        self.assertEqual(analytical_character.database_size,0)
        self.assertEqual(analytical_weapon.database_size,0)

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
        analytical_character.refresh_database_size()
        if not analytical_character.database_is_full():
            database.init_db(self.test_db)
            analytical_character.calculate_and_write_all_solutions()
        
        for i in range(0,analytical_character.max_lookup):
            reverse = analytical_character.lookup_num_to_setting(
                i)
            lookup = analytical_character.lookup_num_generator(
                        reverse[0] , reverse[1] , reverse[2], reverse[3])
            self.assertEqual(i, lookup)
        self.assertTrue(True)

    def test_weapon_lookups_are_invertible(self):
        analytical_weapon = self.analytical_weapon
        analytical_weapon.refresh_database_size()
        if not analytical_weapon.database_is_full():
            analytical_weapon.calculate_and_write_all_solutions()

        for i in range(0,analytical_weapon.max_lookup):
            reverse = analytical_weapon.lookup_num_to_setting(
                i)
            lookup = analytical_weapon.lookup_num_generator(
                        reverse[0] , reverse[1] , reverse[2], reverse[3])
            self.assertEqual(i, lookup)
        self.assertTrue(True)

    def test_probabilities_all_around_one_character(self):
        analytical_character = self.analytical_character
        for i in range(0,analytical_character.max_lookup):
            result = analytical_character.hashtable[i]
            self.assertAlmostEqual(1,sum(result))
        self.assertTrue(True)

    def test_probabilities_all_around_one_weapon(self):
        analytical_weapon = self.analytical_weapon
        for i in range(0,analytical_weapon.max_lookup-1):
            result = analytical_weapon.hashtable[i]
            self.assertAlmostEqual(1,sum(result))
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
        expected_values = values
        self.assertEqual(stat.values, expected_values)
        self.assertEqual(stat.labels, expected_labels)
        self.assertEqual(stat.banner_type, "Character")
    
    def test_create_statistic_weapon(self):
        values = [1,2,3,4,5,6]
        banner_type = "weapon"
        stat = Statistic(values, banner_type)
        expected_labels = ["X"]+["R{}".format(i) for i in range(1,6)]
        expected_values = values
        self.assertEqual(stat.values, expected_values)
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
    
    def test_statistic_get_formatted_init(self):
        values = [1,2,3,4,5,6,7,8]
        banner_type = "character"
        stat = Statistic(values, banner_type,True)
        expected_labels = ["X"]+["C{}".format(i) for i in range(0,7)]
        expected_values = [str(val)+ "."+stat.place_values*"0"  for val in values]
        self.assertEqual(stat.values, expected_values)
        self.assertEqual(stat.labels, expected_labels)
        self.assertEqual(stat.banner_type, "Character")

    def test_statistic_get_data_points(self):
        values = [1,2,3,4,5,6,7,8]
        labels = ["X", "C0","C1","C2","C3","C4","C5","C6"]
        expected_result = [DataPoint(labels[i], values[i]) for i in range(0,len(labels))]
        banner_type = "character"
        stat = Statistic(values, banner_type)
        datapoints = stat.get_data_points()
        self.assertEqual(datapoints, expected_result)

    def test_probability_on_copies_to_num_wishes_character(self):
        analytical_character = self.analytical_character
        numwishes = analytical_character.probability_on_copies_to_num_wishes(.003, 1)
        self.assertEqual(numwishes,1)
    
    def test_probability_on_copies_to_num_wishes_weapon(self):
        analytical_weapon = self.analytical_weapon
        numwishes = analytical_weapon.probability_on_copies_to_num_wishes(.002, 1)
        self.assertEqual(numwishes,1)
    
    def test_database_is_full_on_init_character(self):
        analytical_character = self.analytical_character
        analytical_character_generate = AnalyzeCharacter(self.test_db)


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

    def test_specific_solution_database_full_character(self):
        analytical_character =  self.analytical_character
        analytical_character.hashtable = {}
        result = analytical_character.specific_solution(1,0,0,0,0)
        expected_results = [0.997, 0.003,0.0,0.0,0.0,0.0,0.0,0.0]
        self.assertEqual(result,expected_results)

    

    def test_database_is_full_on_init_weapon(self):
        analytical_weapon = self.analytical_weapon
        analytical_weapon_generate = AnalyzeWeapon(self.test_db)

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

    def test_specific_solution_database_full_weapon(self):
        analytical_weapon =  self.analytical_weapon
        analytical_weapon.hashtable = {}
        result = analytical_weapon.specific_solution(1,0,0,0,0)
        expected_results = [1 - (.006*(.375)), (.006*(.375)),0.0,0.0,0.0,0.0,0.0,0.0]
        for i in range(0,len(result)):
            self.assertAlmostEqual(result[i],expected_results[i])
    
    def test_solution_from_database(self):
        analytical_weapon = self.analytical_weapon
        result = analytical_weapon.solution_from_database(1)
        expected_results = [1 - (.006*(.375)), (.006*(.375)),0.0,0.0,0.0,0.0,0.0,0.0]
        for i in range(0,len(result)):
            self.assertAlmostEqual(result[i],expected_results[i],)
    
    def test_bar_graph_calcprobability_character(self):
        analytical_character =  self.analytical_character
        stat = analytical_character.get_statistic(1,0,0,0,0,False)
        kwargs = {'statistics_type': "calcprobability", "banner_type": "character"}
        bar_graph = bar_graph_for_statistics(stat, **kwargs)
    
    def test_bar_graph_calcprobability_weapon(self):
        analytical_weapon =  self.analytical_weapon
        stat = analytical_weapon.get_statistic(1,0,0,0,0,False)
        kwargs = {'statistics_type': "calcprobability", "banner_type": "weapon"}
        bar_graph = bar_graph_for_statistics(stat, **kwargs)
    
    def test_bar_graph_calcnumwishes_character(self):
        analytical_character = self.analytical_character
        stat = analytical_character.get_statistic(1,0,0,0,0,False)
        kwargs = {'statistics_type': "calcnumwishes", "banner_type": "character"}
        bar_graph = bar_graph_for_statistics(stat, **kwargs)
    
    def test_bar_graph_calcnumwishes_weapon(self):
        analytical_weapon = self.analytical_weapon
        stat = analytical_weapon.get_statistic(1,0,0,0,0, False)
        kwargs = {'statistics_type': "calcnumwishes", "banner_type": "weapon"}
        bar_graph = bar_graph_for_statistics(stat, **kwargs)

    def test_calculate_and_write_solutions_data_already_full(self):
        analytical_character = self.analytical_character
        analytical_character.calculate_and_write_all_solutions()
        analytical_character.refresh_database_size()
        self.assertTrue(analytical_character.database_is_full())
        self.assertEqual(analytical_character.max_lookup, analytical_character.database_size)
        analytical_character.calculate_and_write_all_solutions()
        analytical_character.refresh_database_size()
        self.assertTrue(analytical_character.database_is_full())
        self.assertEqual(analytical_character.max_lookup, analytical_character.database_size)
        expected_result = [.997, 0.003,0,0,0,0,0,0]
        result = analytical_character.specific_solution(1,0,0,0,0)
        for i in range(0,len(expected_result)):
            self.assertAlmostEqual(expected_result, result)

    def test_solution_odds_is_greater_than_last_character_numwishes(self):
        analytical_character = self.analytical_character
        max_pity = analytical_character.hard_pity
        max_wishes_required = analytical_character.max_wishes_required
        fate_points = 0
        for j in range(0, max_pity):
            pity = j
            for k in range(0, 2):
                if k == 0:
                    guaranteed = False
                else:
                    guaranteed = True
                lookup = analytical_character.lookup_num_generator(0,pity,guaranteed,fate_points)
                past = analytical_character.hashtable[lookup]
                sums_past = [sum(past[0:len(past)]) for a in range(0,len(past))]
                for i in range(1, max_wishes_required+1):
                    wish_num = i
                    lookup = analytical_character.lookup_num_generator(wish_num,pity,guaranteed,fate_points)
                    current = analytical_character.hashtable[lookup]
                    sums = [sum(current[0:len(current)]) for a in range(0,len(current))]
                    for a in range(0,len(sums)):
                        self.assertTrue(within_epsilon_or_greater(sums[a],sums_past[a]))
                    sums_past = sums
        self.assertTrue(True)

    def test_solution_odds_is_greater_than_last_weapon_numwishes(self):
        analytical_weapon = self.analytical_weapon
        
        max_pity = analytical_weapon.hard_pity
        max_wishes_required = analytical_weapon.max_wishes_required
        max_fate_points = analytical_weapon.fate_points_required
        
        for j in range(0, max_pity+1):
            pity = j
            for k in range(0, 2):
                for m in range(0, max_fate_points+1):
                    fate_points = m
                    if k == 0:
                        guaranteed = False
                    else:
                        guaranteed = True
                    lookup = analytical_weapon.lookup_num_generator(0,pity,guaranteed,fate_points)
                    past = analytical_weapon.hashtable[lookup]
                    sums_past = [sum(past[0:len(past)]) for a in range(0,len(past))]
                    for j in range(1, max_wishes_required+1):
                        wish_num = j
                        lookup = analytical_weapon.lookup_num_generator(wish_num,pity,guaranteed,fate_points)
                        current  = analytical_weapon.hashtable[lookup]
                        sums = [sum(current[0:len(current)]) for a in range(0,len(current))]
                        for a in range(0,len(sums)):
                            self.assertTrue(within_epsilon_or_greater(sums[a],sums_past[a]))
                        sums_past = sums
        self.assertTrue(True)

    def test_solution_odds_is_greater_than_last_character_pity(self):
        analytical_character = self.analytical_character
        max_pity = analytical_character.hard_pity
        max_wishes_required = analytical_character.max_wishes_required
        fate_points = 0
        for i in range(0, max_wishes_required+1):
            wish_num = i
            for k in range(0, 2):
                if k == 0:
                    guaranteed = False
                else:
                    guaranteed = True
                lookup = analytical_character.lookup_num_generator(wish_num,0,guaranteed,fate_points)
                past = analytical_character.hashtable[lookup]
                sums_past  = [sum(past[0:len(past)]) for a in range(0,len(past))]
                for j in range(1, max_pity+1):
                    pity = j
                    lookup = analytical_character.lookup_num_generator(wish_num,pity,guaranteed,fate_points)
                    current = analytical_character.hashtable[lookup]
                    sums = [sum(current[0:len(current)]) for a in range(0,len(current))]
                    for a in range(0,len(sums)):
                        self.assertTrue(within_epsilon_or_greater(sums[a],sums_past[a]))
                    sums_past = sums
        self.assertTrue(True)

    def test_solution_odds_is_greater_than_last_weapon_pity(self):
        analytical_weapon = self.analytical_weapon
        
        max_pity = analytical_weapon.hard_pity
        max_wishes_required = analytical_weapon.max_wishes_required
        max_fate_points = analytical_weapon.fate_points_required
        
        for i in range(0, max_wishes_required+1):
            wish_num = i
            for k in range(0, 2):
                for m in range(0, max_fate_points+1):
                    fate_points = m
                    if k == 0:
                        guaranteed = False
                    else:
                        guaranteed = True
                    lookup = analytical_weapon.lookup_num_generator(wish_num,0,guaranteed,fate_points)
                    past = analytical_weapon.hashtable[lookup]
                    sums_past  = [sum(past[0:len(past)]) for a in range(0,len(past))]
                    for j in range(1, max_pity+1):
                        pity = j
                        lookup = analytical_weapon.lookup_num_generator(wish_num,pity,guaranteed,fate_points)
                        current = analytical_weapon.hashtable[lookup]
                        sums = [sum(current[0:len(current)]) for a in range(0,len(current))]
                        for a in range(0,len(sums)):
                            self.assertTrue(within_epsilon_or_greater(sums[a],sums_past[a]))
                        sums_past = sums
        self.assertTrue(True)

    def test_solution_odds_is_greater_than_last_character_guaranteed(self):
        analytical_character = self.analytical_character
        max_pity = analytical_character.hard_pity
        max_wishes_required = analytical_character.max_wishes_required
        fate_points = 0
        for i in range(0, max_wishes_required+1):
            wish_num = i
            for j in range(0, max_pity+1):
                pity = j
                lookup = analytical_character.lookup_num_generator(wish_num,pity,False,fate_points)
                past = analytical_character.hashtable[lookup]
                sums_past  = [sum(past[0:len(past)]) for a in range(0,len(past))]
                lookup = analytical_character.lookup_num_generator(wish_num,pity,True,fate_points)
                current = analytical_character.hashtable[lookup]
                sums = [sum(current[0:len(current)]) for a in range(0,len(current))]
                for a in range(0,len(sums)):
                    self.assertTrue(within_epsilon_or_greater(sums[a],sums_past[a]))
        self.assertTrue(True)

    def test_solution_odds_is_greater_than_last_weapon_guaranteed(self):
        analytical_weapon = self.analytical_weapon
        
        max_pity = analytical_weapon.hard_pity
        max_wishes_required = analytical_weapon.max_wishes_required
        max_fate_points = analytical_weapon.fate_points_required
        
        for i in range(0, max_wishes_required+1):
            wish_num = i
            for j in range(0, max_pity+1):
                for m in range(0, max_fate_points+1):
                    fate_points = m
                    pity = j
                    lookup = analytical_weapon.lookup_num_generator(wish_num,pity,False,fate_points)
                    past = analytical_weapon.hashtable[lookup]
                    sums_past  = [sum(past[0:len(past)]) for a in range(0,len(past))]
                    lookup = analytical_weapon.lookup_num_generator(wish_num,pity,True,fate_points)
                    current = analytical_weapon.hashtable[lookup]
                    sums = [sum(current[0:len(current)]) for a in range(0,len(current))]
                    for a in range(0,len(sums)):
                        self.assertTrue(within_epsilon_or_greater(sums[a],sums_past[a]))
        self.assertTrue(True)