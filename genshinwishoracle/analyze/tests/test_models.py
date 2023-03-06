from django.test import TestCase
from ..models import Character, CharacterBanner, Weapon, WeaponBanner
from django.core.management import call_command

class ModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # call_command('loaddata', "analyze/initial_data_character_and_weapons.json", verbosity=0)
        # TODO add a profile with some banners on it maybe? though this mgiht be better to do for the form
        # TODO
        pass

    def setUp(self):
        # TODO
        pass

    
    # -------------------------- CHARACTERS --------------------------

    def test_character_fixture_rationalcontent(self):
        # three limited 4 stars (as of 3.5)
        # 7 non-limited 5 stars (as of 3.5)
        # TODO
        pass

    # -------------------------- WEAPONS --------------------------

    def test_weapon_fixture_rational_content(self):
        # 10 non-limited 5 stars (as of 3.5)
        # TODO
        pass

    # -------------------------- BANNERS --------------------------

    def test_banner_get_specified_banner_equivalent(self):
        # TODO
        pass

    def test_banner_get_all_before_current_date(self):
        # TODO
        pass

    def test_banner_string(self):
        # TODO
        pass

    # -------------------------- CHARACTER BANNERS --------------------------

    def test_characterbanner_get_base_banner_equivalent(self):
        # TODO
        pass

    def test_characterbanner_save(self):
        # TODO
        pass

    def test_characterbanner_string(self):
        # TODO
        pass

    # -------------------------- WEAPON BANNERS --------------------------

    def test_weaponbanner_get_base_banner_equivalent(self):
        # TODO
        pass

    def test_weaponbanner_save(self):
        # TODO
        pass

    def test_weaponbanner_string(self):
        # TODO
        pass
    
