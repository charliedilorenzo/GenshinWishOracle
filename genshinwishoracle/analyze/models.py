from django.db import models
from django.contrib import admin

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
    # Need 1 Five Star and 3 Four Star

    # currently we have only the default pity dist
    # TODO add alternative pity dist
    pity_dist = []
    context_object_name = 'character_banner_identifier'

class WeaponBanner(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length = 64)
    rateups = models.ManyToManyField(Weapon)
    # Need 2 Five Star and 5 Four Star

    # currently we have only the default pity dist
    # TODO add alternative pity dist
    pity_dist = []
    context_object_name = 'weapon_banner_identifier'

# class Question(models.Model):
#     def __str__(self):
#         return self.question_text

#     @admin.display(
#         boolean=True,
#         ordering='pub_date',
#         description='Published recently?',
#     )
#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
