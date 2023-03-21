from django.test import TestCase
from genshinwishoracle import views
from genshinwishoracle.models import Character, Weapon, Banner, WeaponBanner, CharacterBanner
from django.test import Client
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse, reverse_lazy, resolve
from genshinwishoracle.urls import urlpatterns
import math


class ViewsTestClass(TestCase):
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

        testprofile = Profile.objects.filter(user_id=testuser.pk).first()
        testprofile.banners.add(testcharacterbanner)
        testprofile.banners.add(testweaponbanner)

    def setUp(self):
        pass

    # -------------------------- INDEX --------------------------

    def test_IndexView_gives_response(self):
        client = Client()
        response = client.get(reverse('main-home'))
        self.assertEqual(200, response.status_code)
    
    def test_IndexView_context_contains_only_urls_with_views(self):
        client = Client()
        response = client.get(reverse('main-home'))
        context = response.context
        context_object_name = views.IndexView.context_object_name
        urls = context[context_object_name]
        urls_in_urlpatterns = []
        for address in urls:
            self.assertEqual(views.Address, type(address))
            # this will fail with error if there are urls with no views
            resolve(address.url)

    # -------------------------- CHARACTER BANNER --------------------------

    def test_CharacterBannerView_gives_response(self):
        client = Client()
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        response = client.get(reverse('character_banners'), )
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(200, response.status_code)
    
    def test_CharacterBannerView_correct_context(self):
        client = Client()
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        response = client.get(reverse('character_banners'))
        context = response.context
        check_keys = ['labels', 'back_url', 'create_url', 'update_url_front', 'delete_url_front', 'banner_type']
        for item in check_keys:
            self.assertIn(item, context.keys())

        self.assertEqual("Character", context['banner_type'])


    def test_CharacterBannerDeleteView_gives_response(self):
        client = Client()
        banner = CharacterBanner.objects.filter(name=self.characterbannername).first()
        response = client.get(reverse('character_banner_delete', kwargs={'pk': banner.pk}))
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(200, response.status_code)

    def test_CharacterBannerUpdateView_gives_response(self):
        client = Client()
        banner = CharacterBanner.objects.filter(name=self.characterbannername).first()
        response = client.get(reverse('character_banner_update', kwargs={'pk': banner.pk}))
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(200, response.status_code)

    def test_CharacterCreateView_gives_response(self):
        client = Client()
        banner = CharacterBanner.objects.filter(name=self.characterbannername).first()
        response = client.get(reverse('character_banner_create'))
        self.assertEqual(302, response.status_code)

    # -------------------------- WEAPON BANNER --------------------------

    # -------------------------- STATISTICS ANALYZE --------------------------

    # -------------------------- PROJECT PRIMOS  --------------------------

    # -------------------------- WISH SIMULATOR --------------------------
    
