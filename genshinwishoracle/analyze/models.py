from django.db import models
import datetime
from django.utils import timezone
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
    
    def __str__(self) -> str:
        five_stars = self.rateups.filter(rarity=5)
        five_stars = [str(i) for i in five_stars]
        five_star_str = ", ".join(five_stars)
        return "%s - %s - %s" % (self.name,five_star_str, self.enddate)


    def get_base_banner_equivalent(self) -> Banner:
        return self.banner_ptr
    # TODO add query for all banners that are after certain date


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
    
    def __str__(self) -> str:
        five_stars = self.rateups.filter(rarity=5)
        five_stars = [str(i) for i in five_stars]
        five_star_str = ", ".join(five_stars)
        return "%s - %s - %s" % (self.name,five_star_str, self.enddate)

    def get_base_banner_equivalent(self) -> Banner:
        return self.banner_ptr
        # return Banner.objects.filter(id = self.banner_ptr)[0]
    # Need 2 Five Star and 5 Four Star
    # TODO same as character banner