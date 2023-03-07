from django.db import models
import datetime
from django.utils import timezone

class Character(models.Model):
    def __str__(self):
        return self.name
    rarity = models.IntegerField()
    name = models.CharField(max_length= 32)
    limited = models.BooleanField()

    class Meta:
        ordering = ['-rarity', 'name']

class Weapon(models.Model):
    def __str__(self):
        return self.name
    rarity = models.IntegerField()
    name = models.CharField(max_length= 32)
    limited = models.BooleanField()
    class Meta:
        ordering = ['-rarity', 'name']

CHARACTER = "Character"
WEAPON = "Weapon"
BANNER_TYPE = [(CHARACTER, "Character"), (WEAPON, "Weapon"),]

class Banner(models.Model):
    name = models.CharField(max_length = 64)
    enddate = models.DateField()
    banner_type = models.CharField(max_length = 64,choices=BANNER_TYPE)
    # not abstract simply so I can query, but nobody should be making the base Banner class
    def __str__(self):
        specified = self.get_specified_banner_equivalent()
        return str(specified)


    def get_specified_banner_equivalent(self):
        if self.banner_type == CHARACTER:
            found = CharacterBanner.objects.filter(banner_ptr_id=self.id)
            if len(found) > 0:
                return found[0]
            else:
                return None
        elif self.banner_type == WEAPON:
            found = WeaponBanner.objects.filter(banner_ptr_id=self.id)
            if len(found) > 0:
                return found[0]
            else:
                return None
        return None
            
    def get_all_before_current_date(self):
        now = datetime.date.today()
        pass

class CharacterBanner(Banner):
    rateups = models.ManyToManyField(Character,blank=True)
    def save(self, *args, **kwargs):
        self.banner_type = "Character"
        if not self.id:
            newBanner = Banner(name=self.name, enddate=self.enddate,banner_type = self.banner_type)
            super(Banner, newBanner).save(*args, **kwargs)
            self.banner_ptr_id = newBanner.id
        super(CharacterBanner,self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        five_stars = self.rateups.filter(rarity=5)
        five_stars = [str(i) for i in five_stars]
        five_star_str = ", ".join(five_stars)
        return "%s - %s - %s" % (self.name,five_star_str, self.enddate)


    def get_base_banner_equivalent(self) -> Banner:
        return self.banner_ptr
    # TODO add query for all banners that are after certain date
    # currently we have only the default pity dist
    # TODO add alternative pity dist
    # pity_dist = []

    @staticmethod
    def get_banner_type_string() -> str:
        return CHARACTER

class WeaponBanner(Banner):
    # banner_ptr = Banner.objects.create().pk
    rateups = models.ManyToManyField(Weapon,blank=True)
    def save(self, *args, **kwargs):
        self.banner_type = "Weapon"
        if not self.id:
            newBanner = Banner(name=self.name, enddate=self.enddate,banner_type = self.banner_type)
            super(Banner, newBanner).save(*args, **kwargs)
            self.banner_ptr_id = newBanner.id
        super(WeaponBanner,self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        five_stars = self.rateups.filter(rarity=5)
        five_stars = [str(i) for i in five_stars]
        five_star_str = ", ".join(five_stars)
        return "%s - %s - %s" % (self.name,five_star_str, self.enddate)

    def get_base_banner_equivalent(self) -> Banner:
        return self.banner_ptr
        # return Banner.objects.filter(id = self.banner_ptr)[0]

    @staticmethod
    def get_banner_type_string() -> str:
        return WEAPON
    # Need 2 Five Star and 5 Four Star
    # TODO same as character banner