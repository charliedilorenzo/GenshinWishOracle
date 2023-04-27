from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone
from datetime import date

from ..models import Character, CharacterBanner, Weapon, WeaponBanner, Banner
# from genshinwishoracle import settings

class ModelsTestCase(TestCase):
    # fixtures = [settings.BASE_DIR / 'analyze/fixtures/initial_data_characters_and_weapons.json',]
    fixtures = ['initial_data_characters_and_weapons.json',]
    test_username = "testuser"
    test_user_pk = None
    characterbannername = "testbannercharacter"
    weaponbannername = "testbannerweapon"

    def get_test_user(self):
        user = User.objects.filter(username=self.test_username)[0]
        return user

    def get_test_user_profile(self):
        user = self.get_test_user()
        profile = Profile.objects.filter(user_id=user.pk)
        return profile

    @classmethod
    def setUpTestData(cls):
        testuser = User.objects.create_user("testuser", "testemail@gmail.com","verysecurepassword")
        now = timezone.now()
        testcharacterbanner = CharacterBanner.objects.create(name="testbannercharacter", enddate=now, banner_type="Character")
        four_stars = Character.objects.filter(rarity=4)[0:3]
        five_stars = [Character.objects.filter(rarity=5)[0]]
        testcharacterbanner.rateups.add(*four_stars)
        testcharacterbanner.rateups.add(*five_stars)

        testweaponbanner =WeaponBanner.objects.create(name="testbannerweapon", enddate=now, banner_type="Weapon")
        four_stars = Weapon.objects.filter(rarity=4)[0:5]
        five_stars = Weapon.objects.filter(rarity=5)[0:1]
        testweaponbanner.rateups.add(*four_stars)
        testweaponbanner.rateups.add(*five_stars)

    def setUp(self):
        pass

    
    # -------------------------- CHARACTERS --------------------------

    def test_character_fixture_rationalcontent(self):
        # three limited 4 stars (as of 3.5)
        standard_four_stars = ["Amber","Kaeya","Lisa"]
        # 7 non-limited 5 stars (as of 3.5)
        standard_five_stars = ["Dehya","Diluc","Keqing","Jean","Mona","Qiqi", "Tighnari"]

        four_star_check = Character.objects.filter(rarity=4,limited=True)
        for character in four_star_check:
            self.assertIn(character.name,standard_four_stars)
        self.assertEqual(len(four_star_check), len(standard_four_stars))
        self.assertEqual(len(four_star_check),3)
        five_star_check = Character.objects.filter(rarity=5,limited=False)
        for character in five_star_check:
            self.assertIn(character.name,standard_five_stars)
        self.assertEqual(len(five_star_check), len(standard_five_stars))
        self.assertEqual(len(five_star_check), 7)

    # -------------------------- WEAPONS --------------------------

    def test_weapon_fixture_rational_content(self):
        # 7 non-limited 5 stars (as of 3.5)
        standard_five_stars = ["Amos' Bow","Aquila Favonia","Lost Prayer to the Sacred Winds","Primordial Jade Winged-Spear","Skyward Atlas","Skyward Blade","Skyward Harp","Skyward Pride","Skyward Spine","Wolf's Gravestone"]
        five_star_check = Weapon.objects.filter(rarity=5,limited=False)
        for weapon in five_star_check:
            self.assertIn(weapon.name,standard_five_stars)
        self.assertEqual(len(five_star_check), len(standard_five_stars))
        self.assertEqual(len(five_star_check), 10)

    # -------------------------- BANNERS --------------------------

    def test_banner_get_specified_banner_equivalent_character(self):
        testbanner = Banner.objects.filter(name=self.characterbannername)[0]
        specifiedbanner= testbanner.get_specified_banner_equivalent()
        self.assertEqual(type(specifiedbanner), CharacterBanner)
        self.assertEqual(testbanner.name, specifiedbanner.name)
        self.assertEqual(testbanner.enddate, specifiedbanner.enddate)
        self.assertEqual(testbanner.banner_type, specifiedbanner.banner_type)

    def test_banner_get_specified_banner_equivalent_weapon(self):
        testbanner = Banner.objects.filter(name=self.weaponbannername)[0]
        specifiedbanner= testbanner.get_specified_banner_equivalent()
        self.assertEqual(type(specifiedbanner), WeaponBanner)
        self.assertEqual(testbanner.name, specifiedbanner.name)
        self.assertEqual(testbanner.enddate, specifiedbanner.enddate)
        self.assertEqual(testbanner.banner_type, specifiedbanner.banner_type)

    def test_banner_get_specified_banner_equivalent_no_type(self):
        now = timezone.now()
        broken_banner = Banner.objects.create(name="brokenbanner", enddate = now, banner_type = "")
        equiv = broken_banner.get_specified_banner_equivalent()
        self.assertEqual(equiv, None)
        broken_banner.delete()
    
    def test_banner_get_specified_banner_equivalent_typed_character_fail(self):
        now = timezone.now()
        broken_banner = Banner.objects.create(name="brokenbanner", enddate = now, banner_type = "Character")
        equiv = broken_banner.get_specified_banner_equivalent()
        self.assertEqual(equiv, None)
        broken_banner.delete()

    def test_banner_get_specified_banner_equivalent_typed_weapon_fail(self):
        now = timezone.now()
        broken_banner = Banner.objects.create(name="brokenbanner", enddate = now, banner_type = "Weapon")
        equiv = broken_banner.get_specified_banner_equivalent()
        self.assertEqual(equiv, None)
        broken_banner.delete()



    def test_banner_string(self):
        testbanner = Banner.objects.filter(name=self.characterbannername)[0]
        rateup = testbanner.get_specified_banner_equivalent().rateups.filter(rarity=5)[0]
        banner_string = str(testbanner)
        self.assertIn(testbanner.name, banner_string)
        self.assertIn(str(rateup), banner_string)
        self.assertIn(str(testbanner.enddate), banner_string)
        

    # -------------------------- CHARACTER BANNERS --------------------------

    def test_characterbanner_get_base_banner_equivalent(self):
        testbanner = CharacterBanner.objects.filter(name=self.characterbannername)[0]
        basebanner = testbanner.get_base_banner_equivalent()
        self.assertEqual(type(basebanner), Banner)
        self.assertEqual(testbanner.name, basebanner.name)
        self.assertEqual(testbanner.enddate, basebanner.enddate)
        self.assertEqual(testbanner.banner_type, basebanner.banner_type)

    def test_characterbanner_save(self):
        # TODO
        pass

    def test_characterbanner_string(self):
        testbanner = CharacterBanner.objects.filter(name=self.characterbannername)[0]
        rateup = testbanner.rateups.filter(rarity=5)[0]
        banner_string = str(testbanner)
        self.assertIn(testbanner.name, banner_string)
        self.assertIn(str(rateup), banner_string)
        self.assertIn(str(testbanner.enddate), banner_string)

    # -------------------------- WEAPON BANNERS --------------------------

    def test_weaponbanner_get_base_banner_equivalent(self):
        testbanner = WeaponBanner.objects.filter(name=self.weaponbannername)[0]
        basebanner = testbanner.get_base_banner_equivalent()
        self.assertEqual(type(basebanner), Banner)
        self.assertEqual(testbanner.name, basebanner.name)
        self.assertEqual(testbanner.enddate, basebanner.enddate)
        self.assertEqual(testbanner.banner_type, basebanner.banner_type)

    def test_weaponbanner_save(self):
        # TODO
        pass

    def test_weaponbanner_string(self):
        testbanner = WeaponBanner.objects.filter(name=self.weaponbannername)[0]
        rateups = testbanner.rateups.filter(rarity=5)
        banner_string = str(testbanner)
        self.assertIn(testbanner.name, banner_string)
        self.assertIn(str(testbanner.enddate), banner_string)
        for rateup in rateups:
            self.assertIn(str(rateup), banner_string)
    
