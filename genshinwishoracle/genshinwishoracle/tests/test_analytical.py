import os
from genshinwishoracle.analytical import AnalyzeCharacter, AnalyzeWeapon
from django.test import TestCase
from genshinwishoracle import settings
import genshinwishoracle.database as database

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
        assert lookup == -1

    def test_weapon_lookups_above_hard_pity(self):
        analytical_weapon = self.analytical_weapon
        pity = analytical_weapon.hard_pity+1
        wish_num = 1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_negative_num_wish(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = -1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_above_max_wishes(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = analytical_weapon.max_wishes_required+1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_invalid_guaranteed(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = 1
        guaranteed = "False"
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_negative_fate_points(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = 1
        guaranteed = False
        fate_points = -1
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_above_max_fate_points(self):
        analytical_weapon = self.analytical_weapon
        pity = 0
        wish_num = 1
        guaranteed = False
        fate_points = analytical_weapon.fate_points_required+1
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

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
                            assert 0
            assert 1

    # Character Analytical

    def test_character_lookups_negative_pity(self):
        analytical_character = self.analytical_character
        pity = -1
        wish_num = 1
        guaranteed = False
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        assert lookup == -1

    def test_character_lookups_above_hard_pity(self):
        analytical_character = self.analytical_character
        pity = analytical_character.hard_pity+1
        wish_num = 1
        guaranteed = False
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        assert lookup == -1

    def test_character_lookups_negative_num_wish(self):
        analytical_character = self.analytical_character
        pity = 0
        wish_num = -1
        guaranteed = False
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        assert lookup == -1

    def test_character_lookups_above_max_wishes(self):
        analytical_character = self.analytical_character
        pity = 0
        wish_num = analytical_character.max_wishes_required+1
        guaranteed = False
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        assert lookup == -1

    def test_character_lookups_invalid_guaranteed(self):
        analytical_character = self.analytical_character
        pity = 0
        wish_num = 1
        guaranteed = "False"
        fate_points = 0
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed,fate_points)
        assert lookup == -1

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
                        assert 0
            assert 1
