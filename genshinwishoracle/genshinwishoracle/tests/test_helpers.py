from genshinwishoracle.helpers import *
from django.test import TestCase
import pytest

class HelperTestCase(TestCase):
    # ADD DICTIONARIES
    def test_add_list_entries_zero_length(self):
        dicts = [[], []]
        result = add_list_entries(dicts)
        assert result == []

    def test_add_list_entries_many_length_trivial(self):
        dict1 = [ i for i in range(0, 11)]
        dict2 = [0 for i in range(0, 11)]
        expected = dict1.copy()
        dicts = [dict1, dict2]
        result = add_list_entries(dicts)
        assert result == expected

    def test_add_list_entries_many_length_non_trivial(self):
        dict1 = [i*0.1 for i in range(0, 11)]
        dict2 = [1-(i*0.1) for i in range(0, 11)]
        dicts = [dict1, dict2]
        result = add_list_entries(dicts)
        expected = [1 for i in range(0, 11)]
        assert result == expected

    def test_add_list_entries_non_number_value(self):
        dict1 = ["hello"]
        dict2 = [0.5]
        dicts = [dict1, dict2]

        with pytest.raises(Exception) as err:
            result = add_list_entries(dicts)
        assert err.type == TypeError

    def test_add_list_entries_different_lengths(self):
        dict1 = [0.5 for i in range(0, 5)]
        dict2 = dict1.copy()
        dict2.pop(4)
        dicts = [dict1, dict2]

        with pytest.raises(Exception) as err:
            result = add_list_entries(dicts)
        assert err.type == KeyError

    # MULTIPLY DICTIONARIES
    def test_scalar_list_zero_length(self):
        dict = []
        result = scalar_list(dict, 10)
        assert result == []

    def test_scalar_list_scalar_is_zero(self):
        dict = [5000]
        result = scalar_list(dict, 0)
        assert result == [0]

    # UPGRADE DICTIONARIES
    def test_upgrade_list_zero_length(self):
        dict = []
        result = upgrade_list(dict)
        assert result == []

    def test_upgrade_list_one_length(self):
        dict = [1]
        result = upgrade_list(dict)
        assert result == [1]

    def test_upgrade_list_many_length(self):
        dict = [0.25 for i in range(0, 6)]
        expected = dict.copy()
        expected[0] = 0
        expected[5] = 0.5
        result = upgrade_list(dict)
        assert result == expected

    def test_upgrade_list_overupgrading_one_length(self):
        dict = [1]
        result = upgrade_list(dict)
        assert result == [1]

    def test_upgrade_list_overupgrading_many_length(self):
        dict = [0 for i in range(0, 6)]
        dict[5] = 1
        expected = dict.copy()
        result = upgrade_list(dict)
        assert result == expected