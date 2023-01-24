from django.db import models
import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

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

class Banner(models.Model):
    # not abstract simply so I can query, but nobody should be making the base Banner class
    def __str__(self):
        return str(self.get_specified_banner_equivalent())


    def get_specified_banner_equivalent(self):
        attempt_character_banner = CharacterBanner.objects.filter(banner_ptr=self.id)
        if len(attempt_character_banner) == 0:
            return WeaponBanner.objects.filter(banner_ptr=self.id)[0]
        return attempt_character_banner[0]

class CharacterBanner(Banner):
    name = models.CharField(max_length = 64)
    rateups = models.ManyToManyField(Character)
    enddate = models.DateField()

    # Need 1 Five Star and 3 Four Star
    # currently we have only the default pity dist
    # TODO add alternative pity dist
    # pity_dist = []
    def save(self, *args, **kwargs):
        super(Banner, self).save(*args, **kwargs)
        if not self.id:
            newCharBanner = CharacterBanner(name=self.name, rateups=self.rateups.set(), enddate=self.enddate)
            newCharBanner.save()
            self.char_ptr = newCharBanner
    
    def __str__(self):
        five_stars = self.rateups.filter(rarity=5)
        five_stars = [str(i) for i in five_stars]
        five_star_str = ", ".join(five_stars)
        return "%s - %s - %s" % (self.name,five_star_str, self.enddate)


class WeaponBanner(Banner):
    # banner_ptr = Banner.objects.create().pk
    name = models.CharField(max_length = 64)
    rateups = models.ManyToManyField(Weapon)
    enddate = models.DateField()
    def save(self, *args, **kwargs):
        super(Banner, self).save(*args, **kwargs)
        if not self.id:
            newCharBanner = Weapon(name=self.name, rateups=set([]), enddate=self.enddate)
            newCharBanner.save()
            self.char_ptr = newCharBanner
    
    def __str__(self):
        five_stars = self.rateups.filter(rarity=5)
        five_stars = [str(i) for i in five_stars]
        five_star_str = ", ".join(five_stars)
        return "%s - %s - %s" % (self.name,five_star_str, self.enddate)
    # Need 2 Five Star and 5 Four Star
    # TODO same as character banner