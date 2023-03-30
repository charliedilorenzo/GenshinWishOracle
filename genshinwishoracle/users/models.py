from django.db import models
from django.contrib.auth.models import User
import math
from django.conf import settings
from genshinwishoracle.models import Banner, CharacterBanner, WeaponBanner
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet

import genshinwishoracle.models as genshinmodels



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, unique = True, on_delete=models.CASCADE, related_name="profile")
    banners = models.ManyToManyField(Banner)

    numprimos = models.IntegerField(default=0)
    numgenesis = models.IntegerField(default=0)
    numfates = models.IntegerField(default=0)
    numstarglitter = models.IntegerField(default=0)

    character_pity = models.IntegerField(default=0)
    character_guaranteed = models.BooleanField(default=False)

    weapon_pity = models.IntegerField(default=0)
    weapon_guaranteed = models.BooleanField(default=False)
    weapon_fate_points = models.IntegerField(default=0)

    welkin_user = models.BooleanField(default=False)
    battlepass_user = models.BooleanField(default=False)

    def calculate_pure_primos(self):
        return self.numprimos+self.numgenesis+160*math.floor(self.numstarglitter/5) + 160*self.numfates

    def __str__(self):
        return self.user.username
    
    def add_banners(self,banner):
        # self.banners.add(banner)
        # with queryset 
        if isinstance(banner, QuerySet) and len(banner) > 0:
            banner = list(banner)
            for each in banner:
                self.banners.add(each)
        # in list
        elif isinstance(banner, list) and len(banner) > 0:
            for each in banner:
                self.banners.add(each)
        # alone
        elif isinstance(banner,Banner) or isinstance(banner,CharacterBanner) or isinstance(banner, WeaponBanner):
            self.banners.add(banner)
        else:
            raise(Exception)
    
    def user_has_character_banners(self) -> bool: 
        banners = self.banners.all().values_list("banner_type")
        # banners = self.banners.all()
        # print(banners)
        charstring = genshinmodels.CHARACTER
        for banner in banners:
            if banner[0] == charstring:
                return True
        return False

    def user_has_weapon_banners(self) -> bool: 
        banners = self.banners.all().values_list("banner_type")
        weaponstring = genshinmodels.WEAPON
        for banner in banners:
            if banner[0] == weaponstring:
                return True
        return False
