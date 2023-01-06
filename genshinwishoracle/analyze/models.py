from django.db import models
# import datetime
# from django.utils import timezone

class Character(models.Model):
    def __str__(self):
        return self.name
    # TODO make field 3/4/5 only
    # TODO PositiveIntegerField
    rarity = models.IntegerField()
    name = models.CharField(max_length= 32)
    limited = models.BooleanField()

class Weapon(models.Model):
    def __str__(self):
        return self.name
    # TODO make field 3/4/5 only
    # TODO PositiveIntegerField
    rarity = models.IntegerField()
    name = models.CharField(max_length= 32)
    limited = models.BooleanField()

class CharacterBanner(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length = 64)
    rateups = models.ManyToManyField(Character)
    enddate = models.DateField()
    # Need 1 Five Star and 3 Four Star

    # currently we have only the default pity dist
    # TODO add alternative pity dist
    # pity_dist = []

# from analyze.models import CharacterBanner, WeaponBanner
# CharacterBanner.objects.all().delete()

class WeaponBanner(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length = 64)
    rateups = models.ManyToManyField(Weapon)
    enddate = models.DateField()
    # Need 2 Five Star and 5 Four Star

    # currently we have only the default pity dist
    # TODO add alternative pity dist
    # pity_dist = []
