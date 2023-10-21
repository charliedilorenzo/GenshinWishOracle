from django.db import models
from django.contrib.auth.models import User
import math
from django.conf import settings
from django.db.models.query import QuerySet
import datetime

from matplotlib import pyplot 
from io import BytesIO
import base64
from typing import  Union
# from types import UnionTyping

from genshinwishoracle.models import Banner, CharacterBanner, WeaponBanner, CHARACTER, WEAPON, GENERIC

USER_LIMIT_PRIMOGEMSNAPSHOT = 100
USER_LIMIT_BANNER = 15
ADMIN_LIMIT_PRIMOGEMSNAPSHOT = 100000000
ADMIN_LIMIT_BANNER = 100000000

class PrimogemRecord(models.Model):
    def natural_key(self):
        return self.user.natural_key()

    natural_key.dependencies = ["auth.user"]
    # This will function technically as OneToOne but this is simpler to do
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
 
    def get_graph_of_primogem_records(self):
        records = self.primogem_record.get_all_records()
        days_data = []
        primos_data = []
        for record in records:
            days_data.append(record.date)
            primos_data.append(record.primogem_value)

        pyplot.switch_backend('AGG')
        fig, ax = pyplot.subplots(figsize=(10, 6))
        plot = pyplot.plot(days_data,primos_data)
        fig.suptitle('Primo Record')
        fig.supylabel('Number of Primos')
        fig.supxlabel('Date')
        pyplot.tight_layout()

        buffer = BytesIO()
        pyplot.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()
        return graph
   
    def get_all_records(self) -> QuerySet['PrimogemSnapshot']:
        records = PrimogemSnapshot.objects.filter(associated_record_id=self.id)
        return records

    def get_primogem_total(self) -> int:
        current = self.get_all_records().order_by('-id').first()
        if current is not None:
            current = current.primogem_value
        else:
            current = 0
        return current

    def __str__(self) -> str:
        profile = self.get_associated_profile()
        user = User.objects.filter(id=profile.user_id).first()
        string = user.username +"'s Primogem Record - Current Pure Primos: " + str(self.get_primogem_total())
        return string

    def prior_records_today(self) -> QuerySet['PrimogemSnapshot']:
        now = datetime.date.today()
        records = PrimogemSnapshot.objects.filter(associated_record_id=self.id,date=now)
        return records

    def save_new(self,primogem_value: int, superuser: bool) -> Union[None, 'PrimogemSnapshot']:
        now = datetime.date.today()
        prior_records_today = self.prior_records_today()
        # TODO do this in a better way since we just need count not the actual records
        limits_are_okay= self.check_limits(superuser)
        if limits_are_okay:
            # records already exist for today
            if len(prior_records_today) >= 1:
                prior_records_today.delete()
                kwargs = {'primogem_value': primogem_value, 'date': now, 'associated_record': self}
                snapshot = PrimogemSnapshot(**kwargs)
                snapshot.save()
            # records already exist for today
            else:
                kwargs = {'primogem_value': primogem_value, 'date': now, 'associated_record': self}
                snapshot = PrimogemSnapshot(**kwargs)
                snapshot.save()
            return snapshot
        else:
            return None

    def get_associated_profile(self) -> Union['Profile', None]:
        profile = Profile.objects.filter(primogem_record_id=self.id).first()
        return profile
    
    def check_limits(self, superuser: bool) -> bool:
        if superuser:
            return True
        total_record_count = self.get_all_records().count()
        return total_record_count < USER_LIMIT_PRIMOGEMSNAPSHOT


class PrimogemSnapshot(models.Model):
    date = models.DateField()
    associated_record = models.ForeignKey(PrimogemRecord,on_delete=models.CASCADE,null=True)
    primogem_value = models.IntegerField()

    def __str__(self) -> str:
        string = str(self.date) + " : " + str(self.primogem_value)
        return string

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    def create_record_if_none(self) -> None:
        if self.does_user_primogem_record_exists():
            pass
        kwargs = {"user_id": self.user.pk}
        new_record = PrimogemRecord(**kwargs)
        new_record = new_record.save()
        self.primogem_record = new_record
    def natural_key(self):
        return self.user.natural_key()

    natural_key.dependencies = ["auth.user"]
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

    def calculate_pure_primos(self) -> int:
        return self.numprimos+self.numgenesis+160*math.floor(self.numstarglitter/5) + 160*self.numfates

    def __str__(self) -> str:
        return self.user.username
    
    def add_banners(self,banner: Union[QuerySet, list, Banner]):
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
    
    def user_has_any_banner_type(self,banner_type: str) -> bool: 
        # TODO WHat the heck is this
        banners = self.banners.all().values_list("banner_type")
        for banner in banners:
            if banner[0] == banner_type:
                return True
        return False
    
    def get_future_banners(self, banner_type: str = "Banner") -> QuerySet['Banner']:
        acceptable_banner_types  = [CHARACTER, WEAPON, GENERIC]
        if banner_type not in acceptable_banner_types:
            raise Exception(f"Banner type is not one of the allowed types {acceptable_banner_types}")
        now = datetime.date.today()
        if banner_type == GENERIC:
            return self.banners.filter(enddate__gt=now)
        else:
            return self.banners.filter(enddate__gt=now, banner_type=banner_type)
    
    def user_has_any_future_banner(self) -> bool:
        future_banners = self.get_future_banners(banner_type="Banner")
        return future_banners.count() > 0
    
    def does_user_primogem_record_exists(self) -> bool:
        return PrimogemRecord.objects.filter(user_id=self.user.pk).count() >= 1

    def update_primogem_record(self,primogem_value: int) -> Union[None, PrimogemSnapshot]:
        record = self.primogem_record
        superuser = self.user.is_superuser
        return record.save_new(primogem_value,superuser)
    
    def get_user_data_dict(self, fields: list) -> dict:
        # TODO These are used in analyze
        # {'numprimos': curr_user_prof.numprimos, 'numgenesis': curr_user_prof.numgenesis, 'numfates': curr_user_prof.numfates, 'numstarglitter': curr_user_prof.numstarglitter, "battlepass": curr_user_prof.battlepass_user, "welkin_moon": curr_user_prof.welkin_user}
        user_dict = self.__dict__
        return {field: user_dict.get(field) for field in fields}