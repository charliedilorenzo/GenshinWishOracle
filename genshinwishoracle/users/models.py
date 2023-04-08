from django.db import models
from django.contrib.auth.models import User
import math
from django.conf import settings
from genshinwishoracle.models import Banner, CharacterBanner, WeaponBanner
from django.db.models.query import QuerySet

class PrimogemRecord(models.Model):
    def get_all_records(self):
        records = PrimogemSnapshot.objects.filter(associated_record_id=self.id)
        return records

    def get_graph_of_records(self):
        records = self.get_all_records()
        pass

    def get_current_value(self):
        current = self.get_all_records().order_by('-id').first()
        return current

    def __str__(self) -> str:
        records = list(self.get_all_records())
        limit = 20
        i = 0
        record_string = ""
        for record in records:
            if i == limit:
                break
            record_string+= str(record) + "\n"
            i +=1
        return record_string

class PrimogemSnapshot(models.Model):
    date = models.DateField()
    associated_record = models.ForeignKey(PrimogemRecord,on_delete=models.CASCADE,null=True)
    primogem_value = models.IntegerField()

    def __str__(self) -> str:
        string = str(self.date) + " : " + str(self.primogem_value)
        return string

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

    primogem_record = models.OneToOneField(PrimogemRecord, on_delete=models.CASCADE)


    def calculate_pure_primos(self):
        return self.numprimos+self.numgenesis+160*math.floor(self.numstarglitter/5) + 160*self.numfates

    def __str__(self):
        return self.user.username
    
    def add_banners(self,banner):
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
            raise(Exception, "type of add_banners is invalid")
    
    def user_has_any_banner_type(self,banner_type) -> bool: 
        banners = self.banners.all().values_list("banner_type")
        for banner in banners:
            if banner[0] == banner_type:
                return True
        return False