from django.test import TestCase
from genshinwishoracle.models import Character, CharacterBanner, Weapon, WeaponBanner, Banner
import genshinwishoracle.settings
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone
from datetime import date

import math

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

    def test_profile_created_when_user_created(self):
        newuser = User.objects.create_user("newuser", "testemail@gmail.com","verysecurepassword")
        newprofile = Profile.objects.filter(user_id=newuser.pk)
        # was it made?
        self.assertEqual(1,len(newprofile))

        newprofile= newprofile.first()
        profile_dictionary = newprofile.__dict__

        # default fields
        defaults = { "numprimos": 0,
        "numgenesis": 0,
        "numfates": 0,
        "numstarglitter": 0,
        "character_pity": 0,
        "character_guaranteed": False,
        "weapon_pity": 0,
        "weapon_guaranteed": False,
        "weapon_fate_points": 0,
        "welkin_user": False,
        "battlepass_user": False }
        for key in defaults.keys():
            self.assertEqual(defaults[key], profile_dictionary[key])

    def test_calculate_pureprimos(self):
        testprofile = Profile.objects.filter(user_id=User.objects.filter(username=self.test_username).first().pk).first()
        
        # all intertwined fate
        fates = 100
        testprofile.numfates = fates
        self.assertEqual(testprofile.calculate_pure_primos(),fates*160 )

        # all primos
        primos = 1000
        testprofile.numfates = 0
        testprofile.numprimos = primos
        self.assertEqual(testprofile.calculate_pure_primos(),primos )

        # all genesis
        genesis = 1000
        testprofile.numprimos = 0
        testprofile.numgenesis = genesis
        self.assertEqual(testprofile.calculate_pure_primos(),genesis )

        # all starglitter
        starglitter = 100
        testprofile.numgenesis = 0
        testprofile.numstarglitter = starglitter
        self.assertEqual(testprofile.calculate_pure_primos(),math.floor(starglitter/5)*160 )

        # mix 
        fates = 100
        primos = 1000
        genesis = 1000
        starglitter = 100
        testprofile.numstarglitter = 0
        testprofile.numfates = fates
        testprofile.numprimos = primos
        testprofile.numgenesis = genesis
        testprofile.numstarglitter = starglitter
        self.assertEqual(testprofile.calculate_pure_primos(),160*fates+primos+genesis+math.floor(starglitter/5)*160 )

    def test_add_banner_manual(self):
        testprofile = Profile.objects.filter(user_id=User.objects.filter(username=self.test_username).first().pk).first()
        char_banner = CharacterBanner.objects.filter(name=self.characterbannername).first()
        weapon_banner = WeaponBanner.objects.filter(name=self.weaponbannername).first()
        self.assertEqual(len(testprofile.banners.all()),0)
        testprofile.banners.add(char_banner)
        self.assertEqual(len(testprofile.banners.all()),1)
        testprofile.banners.add(weapon_banner)
        self.assertEqual(len(testprofile.banners.all()),2)
        
        different_user = User.objects.create_user("newuser", "testemail@gmail.com","verysecurepassword")
        newprofile = Profile.objects.filter(user_id=different_user.pk).first()

        newprofile.banners.add(char_banner)
        self.assertEqual(len(testprofile.banners.all()),2)
        newprofile.banners.add(weapon_banner)
        self.assertEqual(len(testprofile.banners.all()),2)

    def test_add_banner_method(self):
        # TODO
        pass
        