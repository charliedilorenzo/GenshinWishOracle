from django.test import TestCase
from genshinwishoracle.models import Character, CharacterBanner, Weapon, WeaponBanner
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone

import genshinwishoracle.models as genshinmodels
class ViewsTestCase(TestCase):
    # fixtures = [settings.BASE_DIR / 'analyze/fixtures/initial_data_characters_and_weapons.json',]
    fixtures = ['initial_data_characters_and_weapons.json',]
    test_username = "testuser"
    test_user_pk = None
    characterbannername = "testbannercharacter"
    weaponbannername = "testbannerweapon"
    secondusername = "seconduser"

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

        seconduser = User.objects.create_user("seconduser", "secondemail@gmail.com","verysecurepassword")

    def setUp(self):
        pass
