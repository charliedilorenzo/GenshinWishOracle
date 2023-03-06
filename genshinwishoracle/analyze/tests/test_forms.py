from django.test import TestCase
from .. import forms
from django.core.management import call_command
from django.utils import timezone

class FormsTestCase(TestCase):
    fixtures = ['initial_data_characters_and_weapons.json',]
    @classmethod
    def setUpTestData(cls):
        # TODO add a profile with some banners on it maybe? though this mgiht be better to do for the form
        # TODO
        pass

    # -------------------------- CREATE CHARACTER FORM  --------------------------

    def test_characterform_init_userid(self):
        # TODO
        pass

    def test_characterform_init_no_userid(self):
        # TODO
        pass

    def test_characterform_unique_name_for_user_true(self):
        # TODO
        pass

    def test_characterform_unique_name_for_user_false(self):
        # TODO
        pass

    def test_characterform_verify_rateups_true(self):
        # TODO
        pass

    def test_characterform_verify_rateups_false(self):
        # TODO
        pass

    def test_characterform_is_valid_true(self):
        # TODO
        pass

    def test_characterform_is_valid_false(self):
        # TODO
        pass

    def test_characterform_get_rateup_requirements(self):
        # TODO
        pass

    def test_characterform_save_no_userid(self):
        # TODO
        pass

    def test_characterform_save_userid(self):
        # TODO
        pass

    # -------------------------- CREATE WEAPON FORM  --------------------------

    def test_weaponform_init_userid(self):
        # TODO
        pass

    def test_weaponform_init_no_userid(self):
        # TODO
        pass

    def test_weaponform_unique_name_for_user_true(self):
        # TODO
        pass

    def test_weaponform_unique_name_for_user_false(self):
        # TODO
        pass

    def test_weaponform_verify_rateups_true(self):
        # TODO
        pass

    def test_weaponform_verify_rateups_false(self):
        # TODO
        pass

    def test_weaponform_is_valid_true(self):
        # TODO
        pass

    def test_weaponform_is_valid_false(self):
        # TODO
        pass

    def test_weaponform_get_rateup_requirements(self):
        # TODO
        pass

    def test_weaponform_save_no_userid(self):
        # TODO
        pass

    def test_weaponform_save_userid(self):
        # TODO
        pass


    # -------------------------- STATISTICS TO PROBABILITY CHARACTER  --------------------------

    # -------------------------- STATISTICS TO PROBABILITY WEAPON  --------------------------

    # -------------------------- STATISTICS TO NUM OF WISHES CHARACTER  --------------------------

    # -------------------------- STATISTICS TO NUM OF WISHES WEAPON  --------------------------

    # -------------------------- PROJECT PRIMOS  --------------------------

    def test_projectprimos_init_userid(self):
        # TODO
        pass

    def test_projectprimos_init_no_userid(self):
        # TODO
        pass

    def test_projectprimos_manual_date_is_default_true(self):
        # TODO
        pass
    def test_projectprimos_manual_date_is_default_false(self):
        # TODO
        pass
    
    def test_projectprimos_date_is_decidable_true_manual(self):
        # TODO
        pass

    def test_projectprimos_date_is_decidable_true_banner(self):
        # TODO
        pass

    def test_projectprimos_date_is_decidable_false_both_changed(self):
        # TODO
        pass

    def test_projectprimos_date_is_decidable_false_neither_changed(self):
        # TODO
        pass

    def test_projectprimos_decide_date_manual(self):
        # TODO
        pass
    def test_projectprimos_decide_date_banner(self):
        # TODO
        pass
    def test_projectprimos_decide_date_none(self):
        # TODO
        pass
    
    def test_projectprimos_is_valid_true(self):
        # TODO
        pass
    def test_projectprimos_is_valid_false(self):
        # TODO
        pass

    def test_projectprimos_clean(self):
        # TODO
        pass

    # -------------------------- WISH SIMULATOR --------------------------