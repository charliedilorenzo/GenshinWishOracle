from django.test import TestCase
import pytest
from django.contrib.auth.models import User

from ..helpers import *
from users.models import Profile

class HelperTestCase(TestCase):
    test_username = "testuser"

    @classmethod
    def setUpTestData(cls):
        test_username = "testuser"
        testuser = User.objects.create_user(test_username, "testemail@gmail.com","verysecurepassword")
        
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
    
    def test_within_epsilon_or_greater_exact_match(self):
        epsilon = 0.001
        target = 1
        value = 1
        self.assertTrue(within_epsilon_or_greater(value,target,epsilon=epsilon))
    
    def test_within_epsilon_or_greater_greater_case(self):
        epsilon = 0.001
        target = 1
        value = 2
        self.assertTrue(within_epsilon_or_greater(value,target,epsilon=epsilon))
    
    def test_within_epsilon_or_greater_almost_lesser_case(self):
        epsilon = 0.001
        target = 1
        value = .9999
        self.assertTrue(within_epsilon_or_greater(value,target,epsilon=epsilon))
    
    def test_within_epsilon_or_greater_lesser_case(self):
        epsilon = 0.001
        target = 1
        value = .998
        self.assertTrue(not within_epsilon_or_greater(value,target,epsilon=epsilon))

    def test_import_data_character_prob(self):
        user = User.objects.filter(username=self.test_username).first()
        profile = Profile.objects.filter(user_id=user.pk).first()
        form_type = forms.AnalyzeStatisticsCharacterToProbabilityForm
        data = list(import_user_data(profile, form_type).keys())
        expected_fields = ["pity","guaranteed","numwishes"]
        data.sort()
        expected_fields.sort()
        self.assertTupleEqual(tuple(expected_fields),tuple(data))

    def test_import_data_weapon_prob(self):
        user = User.objects.filter(username=self.test_username).first()
        profile = Profile.objects.filter(user_id=user.pk).first()
        form_type = forms.AnalyzeStatisticsWeaponToProbabilityForm
        data = list(import_user_data(profile, form_type).keys())
        expected_fields = ["pity","guaranteed","fate_points","numwishes"]
        data.sort()
        expected_fields.sort()
        self.assertTupleEqual(tuple(expected_fields),tuple(data))
    
    def test_import_data_character_wishes(self):
        user = User.objects.filter(username=self.test_username).first()
        profile = Profile.objects.filter(user_id=user.pk).first()
        form_type = forms.AnalyzeStatisticsCharacterToNumWishesForm
        data = list(import_user_data(profile, form_type).keys())
        expected_fields = ["pity","guaranteed"]
        data.sort()
        expected_fields.sort()
        self.assertTupleEqual(tuple(expected_fields),tuple(data))
    
    def test_import_data_character_wishes(self):
        user = User.objects.filter(username=self.test_username).first()
        profile = Profile.objects.filter(user_id=user.pk).first()
        form_type = forms.AnalyzeStatisticsWeaponToNumWishesForm
        data = list(import_user_data(profile, form_type).keys())
        expected_fields = ["pity","guaranteed","fate_points"]
        data.sort()
        expected_fields.sort()
        self.assertTupleEqual(tuple(expected_fields),tuple(data))