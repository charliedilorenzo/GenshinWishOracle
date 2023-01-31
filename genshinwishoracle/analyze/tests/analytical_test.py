import pytest
import os
from analyze.analytical import AnalyticalCharacter, AnalyticalWeapon


class TestClass:
    # normally bad practice but this is fine for using the lookup functions
    analytical_weapon = AnalyticalWeapon({})
    analytical_character = AnalyticalCharacter({})
    # Weapon Analytical

    def test_weapon_lookups_negative_pity(self):
        analytical_weapon = AnalyticalWeapon({})
        pity = -1
        wish_num = 1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_above_hard_pity(self):
        analytical_weapon = AnalyticalWeapon({})
        pity = analytical_weapon.hard_pity+1
        wish_num = 1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_negative_num_wish(self):
        analytical_weapon = AnalyticalWeapon({})
        pity = 0
        wish_num = -1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_above_max_wishes(self):
        analytical_weapon = AnalyticalWeapon({})
        pity = 0
        wish_num = analytical_weapon.max_wishes_required+1
        guaranteed = False
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_invalid_guaranteed(self):
        analytical_weapon = AnalyticalWeapon({})
        pity = 0
        wish_num = 1
        guaranteed = "False"
        fate_points = 0
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_negative_fate_points(self):
        analytical_weapon = AnalyticalWeapon({})
        pity = 0
        wish_num = 1
        guaranteed = False
        fate_points = -1
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_above_max_fate_points(self):
        analytical_weapon = AnalyticalWeapon({})
        pity = 0
        wish_num = 1
        guaranteed = False
        fate_points = analytical_weapon.fate_points_required+1
        lookup = analytical_weapon.lookup_num_generator(
            wish_num, pity, guaranteed, fate_points)
        assert lookup == -1

    def test_weapon_lookups_are_invertible(self):
        # this also tests that all values are non-errored into a -1
        analytical_weapon = AnalyticalWeapon({})
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
        analytical_character = AnalyticalCharacter({})
        pity = -1
        wish_num = 1
        guaranteed = False
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed)
        assert lookup == -1

    def test_character_lookups_above_hard_pity(self):
        analytical_character = AnalyticalCharacter({})
        pity = analytical_character.hard_pity+1
        wish_num = 1
        guaranteed = False
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed)
        assert lookup == -1

    def test_character_lookups_negative_num_wish(self):
        analytical_character = AnalyticalCharacter({})
        pity = 0
        wish_num = -1
        guaranteed = False
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed)
        assert lookup == -1

    def test_character_lookups_above_max_wishes(self):
        analytical_character = AnalyticalCharacter({})
        pity = 0
        wish_num = analytical_character.max_wishes_required+1
        guaranteed = False
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed)
        assert lookup == -1

    def test_character_lookups_invalid_guaranteed(self):
        analytical_character = AnalyticalCharacter({})
        pity = 0
        wish_num = 1
        guaranteed = "False"
        lookup = analytical_character.lookup_num_generator(
            wish_num, pity, guaranteed)
        assert lookup == -1

    def test_character_lookups_are_invertible(self):
        analytical_character = AnalyticalCharacter({})
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
                    lookup = analytical_character.lookup_num_generator(
                        wish_num, pity, guaranteed)
                    reverse = analytical_character.lookup_num_to_setting(
                        lookup)
                    if not (wish_num == reverse[0] and pity == reverse[1] and guaranteed == reverse[2]):
                        assert 0
            assert 1
