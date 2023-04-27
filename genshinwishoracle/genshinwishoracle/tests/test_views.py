from django.test import TestCase
import genshinwishoracle.views as views
from django.test import Client
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse, reverse_lazy, resolve
import math
from django.db.models import Q

from ..models import Character, Weapon, Banner, WeaponBanner, CharacterBanner
# from ..urls import urlpatterns

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
        # USER 1
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

        # USER 2
        seconduser = User.objects.create_user("testusertwo", "testemailtwo@gmail.com","verysecurepassword")
        secondprofile = Profile.objects.filter(user_id=seconduser.pk).first()

        testcharacterbannertwo = CharacterBanner.objects.create(name="secondbannercharacter", enddate=now, banner_type="Character")
        four_stars = Character.objects.filter(rarity=4)[0:3]
        five_stars = [Character.objects.filter(rarity=5)[0]]
        testcharacterbannertwo.rateups.add(*four_stars)
        testcharacterbannertwo.rateups.add(*five_stars)

        testweaponbannertwo =WeaponBanner.objects.create(name="secondbannerweapon", enddate=now, banner_type="Weapon")
        four_stars = Weapon.objects.filter(rarity=4)[0:5]
        five_stars = Weapon.objects.filter(rarity=5)[0:1]
        testweaponbannertwo.rateups.add(*four_stars)
        testweaponbannertwo.rateups.add(*five_stars)

        secondprofile.banners.add(testcharacterbannertwo)
        secondprofile.banners.add(testweaponbannertwo)

    def setUp(self):
        pass

    # -------------------------- INDEX --------------------------

    def test_IndexView_gives_response(self):
        response = self.client.get(reverse('main-home'))
        self.assertEqual(200, response.status_code)
    
    def test_IndexView_context_contains_only_urls_with_views(self):
        client = self.client
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

    # Only testing here for login cause it should be the same for all the banner views
    def test_CharacterBannerView_redirect_not_logged_in(self):
        client = self.client
        response = client.get(reverse('character_banners'))
        self.assertRedirects(response, reverse_lazy('login')+"?"+views.PersonalizedLoginRequiredMixin.redirect_field_name+"="+reverse('character_banners'))
        response = client.post(reverse('character_banners'))
        self.assertRedirects(response, reverse_lazy('login')+"?"+views.PersonalizedLoginRequiredMixin.redirect_field_name+"="+reverse('character_banners'))

    def test_CharacterBannerView_login_gives_response(self):
        client = self.client
        user = User.objects.filter(username = self.test_username).first()
        client.force_login(user)
        response = client.get(reverse('character_banners'), )
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(200, response.status_code)
    
    def test_CharacterBannerView_correct_context_keys(self):
        client = self.client
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        response = client.get(reverse('character_banners'))
        context = response.context
        check_keys = ['labels', 'back_url', 'create_url', 'url_front', 'banner_type']
        for item in check_keys:
            self.assertIn(item, context.keys())

        self.assertEqual("Character", context['banner_type'])

    def test_CharacterBannerView_correct_banners(self):
        client = self.client
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        response = client.get(reverse('character_banners'))
        context = response.context
        banners = context['banners']
        testuser_banners = Profile.objects.filter(user_id=user.pk).first().banners.filter(banner_type="Character")
        for banner in banners:
            banner_in = banner.get_base_banner_equivalent() in testuser_banners
            if banner_in:
                self.assertTrue(True)
            else:
                self.assertTrue(False)

    def test_CharacterBannerDeleteView_redirect_non_existent_banner(self):
        client = self.client
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        
        # create and delete to have an invalid pk
        now = timezone.now()
        testcharacterbanner = CharacterBanner.objects.create(name="testbannercharacter", enddate=now, banner_type="Character")
        four_stars = Character.objects.filter(rarity=4)[0:3]
        five_stars = [Character.objects.filter(rarity=5)[0]]
        testcharacterbanner.rateups.add(*four_stars)
        testcharacterbanner.rateups.add(*five_stars)
        pk = testcharacterbanner.pk
        testcharacterbanner.delete()

        response = client.get(reverse('character_banner_delete', kwargs={'pk': pk}))
        self.assertEqual(404, response.status_code)

    def test_CharacterBannerDeleteView_not_users_banner(self):
        client = self.client
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        banner = CharacterBanner.objects.filter(~Q(name=self.characterbannername )).first()
        response = client.get(reverse('character_banner_delete', kwargs={'pk': banner.pk}))
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy('character_banners'))

        response = client.post(reverse('character_banner_delete', kwargs={'pk': banner.pk}))
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy('character_banners'))
       

    def test_CharacterBannerDeleteView_gives_response(self):
        client = self.client
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        banner = CharacterBanner.objects.filter(name=self.characterbannername).first()
        response = client.get(reverse('character_banner_delete', kwargs={'pk': banner.pk}))
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(200, response.status_code)

    def test_CharacterBannerUpdateView_redirect_non_existent_banner(self):
        client = self.client
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        
        # create and delete to have an invalid pk
        now = timezone.now()
        testcharacterbanner = CharacterBanner.objects.create(name="testbannercharacter", enddate=now, banner_type="Character")
        four_stars = Character.objects.filter(rarity=4)[0:3]
        five_stars = [Character.objects.filter(rarity=5)[0]]
        testcharacterbanner.rateups.add(*four_stars)
        testcharacterbanner.rateups.add(*five_stars)
        pk = testcharacterbanner.pk
        testcharacterbanner.delete()

        response = client.get(reverse('character_banner_update', kwargs={'pk': pk}))
        self.assertEqual(404, response.status_code)

    def test_CharacterBannerUpdateView_not_users_banner(self):
        client = self.client
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        banner = CharacterBanner.objects.filter(~Q(name=self.characterbannername )).first()
        response = client.get(reverse('character_banner_update', kwargs={'pk': banner.pk}))
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy('character_banners'))

        response = client.post(reverse('character_banner_update', kwargs={'pk': banner.pk}))
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy('character_banners'))

    def test_CharacterBannerUpdateView_gives_response(self):
        client = self.client
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        banner = CharacterBanner.objects.filter(name=self.characterbannername).first()
        response = client.get(reverse('character_banner_update', kwargs={'pk': banner.pk}))
        self.assertTrue(math.floor(response.status_code / 100 ) != 4)
        self.assertEqual(200, response.status_code)

    def test_CharacterCreateView_gives_response(self):
        client = self.client
        user = User.objects.filter(username=self.test_username).first()
        client.force_login(user)
        banner = CharacterBanner.objects.filter(name=self.characterbannername).first()
        response = client.get(reverse('character_banner_create'))
        self.assertEqual(200, response.status_code)

    # -------------------------- WEAPON BANNER --------------------------
    # TODO later, lower priority since character and weapon are similar
    # -------------------------- STATISTICS ANALYZE --------------------------

    # -------------------------- PROJECT PRIMOS  --------------------------
    
    # -------------------------- WISH SIMULATOR --------------------------
    
