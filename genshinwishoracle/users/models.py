from django.db import models
from django.contrib.auth.models import User
import math
from django.conf import settings
from analyze.models import Banner

class CustomUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    banners = models.ManyToManyField(Banner)

    numprimos = models.IntegerField()
    numgenesis = models.IntegerField()
    numfates = models.IntegerField()
    numstarglitter = models.IntegerField()

    character_pity = models.IntegerField()
    character_guaranteed = models.BooleanField()
    character_fate_points = models.IntegerField()

    weapon_pity = models.IntegerField()
    weapon_guaranteed = models.BooleanField()
    weapon_fate_points = models.IntegerField()

    welkin_user = models.BooleanField()
    battlepass_user = models.BooleanField()

    def calculate_pure_primos(self):
        return self.numprimos+self.numgenesis+160*math.floor(self.numstarglitter/5) + 160*self.numfates