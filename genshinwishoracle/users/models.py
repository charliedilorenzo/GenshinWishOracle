from django.db import models
from django.contrib.auth.models import User
import math
from django.conf import settings
from genshinwishoracle.models import Banner

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
    
    def add_banner(self):
        # TODO
        pass