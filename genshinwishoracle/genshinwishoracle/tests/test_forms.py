from django.test import TestCase
from genshinwishoracle import forms
from genshinwishoracle.models import Character, CharacterBanner, Weapon, WeaponBanner, Banner
from django.core.management import call_command
from django.utils import timezone
from users.models import Profile
from django.contrib.auth.models import User
from datetime import date

class FormsTestCase(TestCase):
    fixtures = ['initial_data_characters_and_weapons.json',]
    test_username = "testuser"
    characterbannername = "testbannercharacter"
    weaponbannername = "testbannerweapon"
    character_four_requirements = 3
    character_five_requirements = 1
    weapon_four_requirements = 5
    weapon_five_requirements = 2

    def get_characters(self):
        four_stars = Character.objects.filter(rarity=4)[0:self.character_four_requirements]
        five_stars = Character.objects.filter(rarity=5)[0:self.character_five_requirements]
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Character.objects.filter(id__in=ids)
        return rateups

    def get_weapons(self):
        four_stars = Weapon.objects.filter(rarity=4)[0:self.weapon_four_requirements]
        five_stars = Weapon.objects.filter(rarity=5)[0:self.weapon_five_requirements]
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Weapon.objects.filter(id__in=ids)
        return rateups

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

    # -------------------------- CREATE CHARACTER FORM  --------------------------

    def test_characterform_init_userid(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_characters()
        now = date.today()
        data = {'rateups': rateups, 'name': "testform", 'enddate': now}

        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        form.is_valid()
        self.assertEqual(form.user_id, testuser.pk)

    def test_characterform_init_no_userid(self):
        testuser = User.objects.filter(username=self.test_username).first()
        rateups = self.get_characters()
        now = date.today()
        data = {'rateups': rateups, 'name': "testform", 'enddate': now}

        form  = forms.CreateCharacterBannerForm(data)
        form.is_valid()
        self.assertEqual(form.user_id, None)

    def test_characterform_unique_name_for_user_true(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_characters()
        now = date.today()
        data = {'rateups': rateups, 'name': "thisnameistotallyuniqueandnobannerhasit", 'enddate': now}

        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        form.is_valid()
        unique = form.unique_name_for_user(data['name'])
        self.assertTrue(unique)

    def test_characterform_unique_name_for_user_false(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_characters()
        now = date.today()
        data = {'rateups': rateups, 'name': self.characterbannername, 'enddate': now}
        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        form.is_valid()
        unique = form.unique_name_for_user(data['name'])
        self.assertTrue(not unique)

    def test_characterform_verify_rateups_true(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()

        rateups = self.get_characters()
        data = {'rateups': rateups, 'name': self.characterbannername, 'enddate': now}
        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(verify)

    def test_characterform_verify_rateups_too_many_four(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        

        four_stars = Character.objects.filter(rarity=4)[0:self.character_four_requirements+1]
        five_stars = Character.objects.filter(rarity=5)[0:self.character_five_requirements]
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Character.objects.filter(id__in=ids)


        data = {'rateups': rateups, 'name': self.characterbannername, 'enddate': now}
        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(not verify)

    def test_characterform_verify_rateups_too_many_five(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        

        four_stars = Character.objects.filter(rarity=4)[0:self.character_four_requirements]
        five_stars = Character.objects.filter(rarity=5)[0:self.character_five_requirements+1]
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Character.objects.filter(id__in=ids)


        data = {'rateups': rateups, 'name': self.characterbannername, 'enddate': now}
        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(not verify)

    def test_characterform_verify_rateups_too_few_four(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        

        four_stars = Character.objects.filter(rarity=4)[0:self.character_four_requirements-1]
        five_stars = Character.objects.filter(rarity=5)[0:self.character_five_requirements]
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Character.objects.filter(id__in=ids)


        data = {'rateups': rateups, 'name': self.characterbannername, 'enddate': now}
        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(not verify)

    def test_characterform_verify_rateups_too_few_five(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        

        four_stars = Character.objects.filter(rarity=4)[0:self.character_four_requirements]
        five_stars = Character.objects.filter(rarity=5).none()
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Character.objects.filter(id__in=ids)


        data = {'rateups': rateups, 'name': self.characterbannername, 'enddate': now}
        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(not verify)

    def test_characterform_is_valid_true(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_characters()
        now = date.today()
        data = {'rateups': rateups, 'name': "testform", 'enddate': now}

        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        valid = form.is_valid()
        self.assertTrue(valid)

    def test_characterform_is_valid_false(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_characters()
        now = date.today()
        data = {'rateups': rateups, 'name': None, 'enddate': now}

        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        valid = form.is_valid()
        self.assertTrue(not valid)

    def test_characterform_get_rateup_requirements(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_characters()
        now = date.today()
        data = {'rateups': rateups, 'name': "testform", 'enddate': now}

        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        requirements_dictionary = form.get_rateup_requirements()
        self.assertEqual({3:0,4:self.character_four_requirements,5:self.character_five_requirements},requirements_dictionary)


    def test_characterform_save_userid(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()

        rateups = self.get_characters()
        data = {'rateups': rateups, 'name': "testingsaveuserid", 'enddate': now}
        form  = forms.CreateCharacterBannerForm(data, **kwargs)
        form.is_valid()
        form.verify_rateups()

        testprofile = Profile.objects.filter(user_id=testuser.pk).first()
        character_banners = CharacterBanner.objects.all()

        former_length_profile = len(testprofile.banners.all())
        former_length_character_banners = len(character_banners)
    
        character_banner = form.save()

        self.assertEqual(former_length_character_banners+1, len(CharacterBanner.objects.all()))

        testprofile.banners.add(character_banner)

        self.assertEqual(former_length_profile+1, len(Profile.objects.filter(user_id=testuser.pk).first().banners.all()))

    # -------------------------- CREATE WEAPON FORM  --------------------------

    def test_weaponform_init_userid(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_weapons()
        now = date.today()
        data = {'rateups': rateups, 'name': "testform", 'enddate': now}

        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        form.is_valid()
        self.assertEqual(form.user_id, testuser.pk)

    def test_weaponform_init_no_userid(self):
        testuser = User.objects.filter(username=self.test_username).first()
        rateups = self.get_weapons()
        now = date.today()
        data = {'rateups': rateups, 'name': "testform", 'enddate': now}

        form  = forms.CreateWeaponBannerForm(data)
        form.is_valid()
        self.assertEqual(form.user_id, None)

    def test_weaponform_unique_name_for_user_true(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_weapons()
        now = date.today()
        data = {'rateups': rateups, 'name': "thisnameistotallyuniqueandnobannerhasit", 'enddate': now}

        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        form.is_valid()
        unique = form.unique_name_for_user(data['name'])
        self.assertTrue(unique)

    def test_weaponform_unique_name_for_user_false(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_weapons()
        now = date.today()
        data = {'rateups': rateups, 'name': self.characterbannername, 'enddate': now}
        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        form.is_valid()
        unique = form.unique_name_for_user(data['name'])
        self.assertTrue(not unique)

    def test_weaponform_verify_rateups_true(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()

        rateups = self.get_weapons()
        data = {'rateups': rateups, 'name': self.weaponbannername, 'enddate': now}
        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(verify)

    def test_weaponform_verify_rateups_too_many_four(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        

        four_stars = Weapon.objects.filter(rarity=4)[0:self.weapon_four_requirements+1]
        five_stars = Weapon.objects.filter(rarity=5)[0:self.weapon_five_requirements]
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Weapon.objects.filter(id__in=ids)


        data = {'rateups': rateups, 'name': self.weaponbannername, 'enddate': now}
        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(not verify)

    def test_weaponform_verify_rateups_too_many_five(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        

        four_stars = Weapon.objects.filter(rarity=4)[0:self.weapon_four_requirements]
        five_stars = Weapon.objects.filter(rarity=5)[0:self.weapon_five_requirements+1]
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Weapon.objects.filter(id__in=ids)


        data = {'rateups': rateups, 'name': self.weaponbannername, 'enddate': now}
        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(not verify)

    def test_weaponform_verify_rateups_too_few_four(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        

        four_stars = Weapon.objects.filter(rarity=4)[0:self.weapon_four_requirements-1]
        five_stars = Weapon.objects.filter(rarity=5)[0:self.weapon_five_requirements]
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Weapon.objects.filter(id__in=ids)


        data = {'rateups': rateups, 'name': self.weaponbannername, 'enddate': now}
        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(not verify)

    def test_weaponform_verify_rateups_too_few_five(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        

        four_stars = Weapon.objects.filter(rarity=4)[0:self.weapon_four_requirements]
        five_stars = Weapon.objects.filter(rarity=5).none()
        ids = [four.id for four in four_stars]+[five.id for five in five_stars]
        rateups = Weapon.objects.filter(id__in=ids)


        data = {'rateups': rateups, 'name': self.weaponbannername, 'enddate': now}
        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        form.is_valid()
        verify = form.verify_rateups()
        self.assertTrue(not verify)

    def test_weaponform_is_valid_true(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_weapons()
        now = date.today()
        data = {'rateups': rateups, 'name': "testform", 'enddate': now}

        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        valid = form.is_valid()
        self.assertTrue(valid)

    def test_weaponform_is_valid_false(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_weapons()
        now = date.today()
        data = {'rateups': rateups, 'name': None, 'enddate': now}

        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        valid = form.is_valid()
        self.assertTrue(not valid)

    def test_weaponform_get_rateup_requirements(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_weapons()
        now = date.today()
        data = {'rateups': rateups, 'name': "testform", 'enddate': now}

        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        requirements_dictionary = form.get_rateup_requirements()
        self.assertEqual({3:0,4:self.weapon_four_requirements,5:self.weapon_five_requirements},requirements_dictionary)


    def test_weaponform_save_userid(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()

        rateups = self.get_weapons()
        data = {'rateups': rateups, 'name': "testingsaveuserid", 'enddate': now}
        form  = forms.CreateWeaponBannerForm(data, **kwargs)
        form.is_valid()
        form.verify_rateups()

        testprofile = Profile.objects.filter(user_id=testuser.pk).first()
        weapon_banners = WeaponBanner.objects.all()

        former_length_profile = len(testprofile.banners.all())
        former_length_weapon_banners = len(weapon_banners)
    
        weapon_banner = form.save()

        self.assertEqual(former_length_weapon_banners+1, len(WeaponBanner.objects.all()))

        testprofile.banners.add(weapon_banner)

        self.assertEqual(former_length_profile+1, len(Profile.objects.filter(user_id=testuser.pk).first().banners.all()))


    # -------------------------- STATISTICS TO PROBABILITY CHARACTER  --------------------------

    # -------------------------- STATISTICS TO PROBABILITY WEAPON  --------------------------

    # -------------------------- STATISTICS TO NUM OF WISHES CHARACTER  --------------------------

    # -------------------------- STATISTICS TO NUM OF WISHES WEAPON  --------------------------

    # -------------------------- PROJECT PRIMOS  --------------------------
    def test_projectprimos_is_valid_true(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(now)
        data['end_date_banner_select'] = None


        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        self.assertEqual(form.user_id, testuser.pk)
    
    def test_projectprimos_init_userid(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(now)
        data['end_date_banner_select'] = None


        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        self.assertEqual(form.user_id, testuser.pk)

    def test_projectprimos_init_no_userid(self):
        testuser = User.objects.filter(username=self.test_username).first()
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(now)
        # data['end_date_banner_select'] = None

        form  = forms.ProjectPrimosForm(data)
        form.is_valid()
        self.assertEqual(form.user_id, None)

    def test_projectprimos_manual_date_is_default_true(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_characters()
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year,1,1))
        data['end_date_banner_select'] = None

        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        default = form.manual_select_is_default()
        self.assertTrue(default)


    def test_projectprimos_manual_date_is_default_false(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        rateups = self.get_characters()
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year,2,1))
        data['end_date_banner_select'] = None

        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        default = form.manual_select_is_default()
        self.assertTrue(not default)
    
    def test_projectprimos_date_is_decidable_true_manual(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year,2,1))
        data['end_date_banner_select'] = None

        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        decidable = form.date_is_decidable()
        self.assertTrue(decidable)

    def test_projectprimos_date_is_decidable_true_banner(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year,1,1))
        testprofile = Profile.objects.filter(user_id = testuser.pk).first()
        data['end_date_banner_select'] = testprofile.banners.filter(enddate__gte=now).first()

        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        decidable = form.date_is_decidable()
        self.assertTrue(decidable)

    def test_projectprimos_date_is_decidable_false_both_changed(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year+1,2,1))
        testprofile = Profile.objects.filter(user_id = testuser.pk).first()
        data['end_date_banner_select'] = testprofile.banners.filter(enddate__gte=now).first()
        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        decidable = form.date_is_decidable()
        self.assertTrue(not decidable)

    def test_projectprimos_date_is_decidable_false_neither_changed(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year,1,1))
        data['end_date_banner_select'] = None

        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        decidable = form.date_is_decidable()
        self.assertTrue(not decidable)

    def test_projectprimos_decide_date_manual(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        testdate = date(now.year,2,1)
        data['end_date_manual_select'] = str(testdate)
        data['end_date_banner_select'] = None

        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        decision = form.decide_date()
        self.assertEqual(testdate, decision)

    def test_projectprimos_decide_date_banner(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year,1,1))
        testprofile = Profile.objects.filter(user_id = testuser.pk).first()
        data['end_date_banner_select'] = testprofile.banners.filter(enddate__gte=now).first()

        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        decision = form.decide_date()
        self.assertEqual(data['end_date_banner_select'].enddate, decision)

    def test_projectprimos_decide_date_none(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year+1,2,1))
        testprofile = Profile.objects.filter(user_id = testuser.pk).first()
        data['end_date_banner_select'] = testprofile.banners.filter(enddate__gte=now).first()
        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        decision = form.decide_date()
        self.assertEqual(None, decision)
    
    def test_projectprimos_is_valid_true(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': 0, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year,2,1))
        data['end_date_banner_select'] = None

        form  = forms.ProjectPrimosForm(data, **kwargs)
        valid = form.is_valid()
        self.assertTrue(valid)


    def test_projectprimos_is_valid_false(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': -3, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year,2,1))
        data['end_date_banner_select'] = None

        form  = forms.ProjectPrimosForm(data, **kwargs)
        valid = form.is_valid()
        self.assertTrue(not valid)

    def test_projectprimos_clean(self):
        testuser = User.objects.filter(username=self.test_username).first()
        kwargs = {'user_id': testuser.pk}
        now = date.today()
        data = {'numprimos': -3, 'numgenesis': 0, 'numfates': 0 , 'numstarglitter': 0 , 'welkin_moon': True,'battlepass': True, 'average_abyss_stars': 30}
        data['end_date_manual_select'] = str(date(now.year,2,1))
        data['end_date_banner_select'] = None

        form  = forms.ProjectPrimosForm(data, **kwargs)
        form.is_valid()
        cleaned = form.clean()
        self.assertTrue(data, cleaned)

    # -------------------------- WISH SIMULATOR --------------------------