import pytest

from analyze.helpers import *
from django.test import TestCase

class HelperTestCase(TestCase):
    # ADD DICTIONARIES
    def test_add_dictionary_entries_zero_length(self):
        dicts = [{}, {}]
        result = add_dictionary_entries(dicts)
        assert result == {}

    def test_add_dictionary_entries_many_length_trivial(self):
        dict1 = {i: i for i in range(0, 11)}
        dict2 = {i: 0 for i in range(0, 11)}
        expected = dict1.copy()
        dicts = [dict1, dict2]
        result = add_dictionary_entries(dicts)
        assert result == expected

    def test_add_dictionary_entries_many_length_non_trivial(self):
        dict1 = {i: i*0.1 for i in range(0, 11)}
        dict2 = {i: 1-(i*0.1) for i in range(0, 11)}
        dicts = [dict1, dict2]
        result = add_dictionary_entries(dicts)
        expected = {i: 1 for i in range(0, 11)}
        assert result == expected

    def test_add_dictionary_entries_non_number_value(self):
        dict1 = {0: "hello"}
        dict2 = {0: 0.5}
        dicts = [dict1, dict2]

        with pytest.raises(Exception) as err:
            result = add_dictionary_entries(dicts)
        assert "Dictionary contains keys that are neither intergers nor floats" in str(
            err.value)
        assert err.type == TypeError

    def test_add_dictionary_entries_different_lengths(self):
        dict1 = {i: 0.5 for i in range(0, 5)}
        dict2 = dict1.copy()
        dict2.pop(4)
        dicts = [dict1, dict2]

        with pytest.raises(Exception) as err:
            result = add_dictionary_entries(dicts)
        assert err.type == KeyError

    def test_add_dictionary_entries_different_keys(self):
        dict1 = {i: 0.5 for i in range(0, 5)}
        dict2 = dict1.copy()
        dict2.pop(0)
        dict2[5] = 0.5
        dicts = [dict1, dict2]

        with pytest.raises(Exception) as err:
            result = add_dictionary_entries(dicts)
        assert err.type == KeyError

    # MULTIPLY DICTIONARIES
    def test_multiply_dictionary_entries_zero_length(self):
        dict = {}
        result = multiply_dictionary_entries(dict, 10)
        assert result == {}

    def test_multiply_dictionary_entries_scalar_is_zero(self):
        dict = {1: 5000}
        result = multiply_dictionary_entries(dict, 0)
        assert result == {1: 0}

    # UPGRADE DICTIONARIES
    def test_upgrade_dictionary_zero_length(self):
        dict = {}
        result = upgrade_dictionary(dict)
        assert result == {}

    def test_upgrade_dictionary_one_length(self):
        dict = {0: 1}
        result = upgrade_dictionary(dict)
        assert result == {0: 1}

    def test_upgrade_dictionary_many_length(self):
        dict = {i: 0.25 for i in range(0, 6)}
        expected = dict.copy()
        expected[0] = 0
        expected[5] = 0.5
        result = upgrade_dictionary(dict)
        assert result == expected

    def test_upgrade_dictionary_overupgrading_one_length(self):
        dict = {0: 1}
        result = upgrade_dictionary(dict)
        assert result == {0: 1}

    def test_upgrade_dictionary_overupgrading_many_length(self):
        dict = {i: 0 for i in range(0, 6)}
        dict[5] = 1
        expected = dict.copy()
        result = upgrade_dictionary(dict)
        assert result == expected

    def test_upgrade_dictionary_non_number_value_one_length(self):
        dict = {0: "hello"}

        with pytest.raises(Exception) as err:
            result = upgrade_dictionary(dict)
        assert "Dictionary contains keys that are neither integers nor floats" in str(
            err.value)
        assert err.type == TypeError

    def test_upgrade_dictionary_non_number_value_many_length_zero_index(self):
        dict = {i: .25 for i in range(0, 6)}
        dict[0] = "hello"

        with pytest.raises(Exception) as err:
            result = upgrade_dictionary(dict)
        assert "Dictionary contains keys that are neither integers nor floats" in str(
            err.value)
        assert err.type == TypeError

    def test_upgrade_dictionary_non_number_value_many_length_middle(self):
        dict = {i: .25 for i in range(0, 6)}
        dict[3] = "hello"

        with pytest.raises(Exception) as err:
            result = upgrade_dictionary(dict)
        assert "Dictionary contains keys that are neither integers nor floats" in str(
            err.value)
        assert err.type == TypeError

    def test_upgrade_dictionary_non_number_value_many_length_penultimate(self):
        dict = {i: .25 for i in range(0, 6)}
        dict[4] = "hello"

        with pytest.raises(Exception) as err:
            result = upgrade_dictionary(dict)
        assert "Dictionary contains keys that are neither integers nor floats" in str(
            err.value)
        assert err.type == TypeError

    def test_upgrade_dictionary_non_number_value_many_length_final(self):
        dict = {i: .25 for i in range(0, 6)}
        dict[5] = "hello"

        with pytest.raises(Exception) as err:
            result = upgrade_dictionary(dict)
        assert "Dictionary contains keys that are neither integers nor floats" in str(
            err.value)
        assert err.type == TypeError

    def test_upgrade_dictionary_gap_in_keys(self):
        dict = {0: .25, 1: .25, 3: .25, 4: .25}
        with pytest.raises(Exception) as err:
            result = upgrade_dictionary(dict)
        assert err.type == KeyError
