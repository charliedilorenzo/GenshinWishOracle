from django import forms
from . import models
from .validators import validate_character_rateups
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
import datetime

class CreateCharacterBannerForm(forms.ModelForm):
    class Meta:
        model = models.CharacterBanner
        fields = ['name', 'rateups', 'enddate']
    name = forms.CharField(max_length = 64)
    # rateups = forms.ModelMultipleChoiceField(
        # queryset=models.Character.objects.all(),
        # widget=forms.MultiWidget(widgets=[forms.Select, forms.Select, forms.Select, forms.Select])
    # )
    rateups = forms.ModelMultipleChoiceField(
        queryset=models.Character.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': 30}),
        validators=[validate_character_rateups]  
    )
    enddate = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))

class CreateWeaponBannerForm(forms.ModelForm):
    class Meta:
        model = models.WeaponBanner
        fields = ['name', 'rateups', 'enddate']
    name = forms.CharField(max_length = 64)
    rateups = forms.ModelMultipleChoiceField(
        queryset=models.Weapon.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': 30})
        # TODO add validator
    )
    enddate = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))

class AnalyzeStatisticsCharacterToProbabilityForm(forms.Form):
    class Meta:
        fields = ['numwishes', 'pity', 'guaranteed']
    numwishes = forms.IntegerField(label="Number of wishes", min_value=0,error_messages={'required': "Please add your number of wishes", 'min_value': "Number of wishes must be greater than 0"})
    pity = forms.IntegerField(label="Pity",max_value=90,min_value=0, initial=0, required=False, error_messages={'min_value': "Pity must be between 0 and 90", 'max_value': "Pity must be between 0 and 90"})
    guaranteed = forms.BooleanField(label="Have Guaranteed",initial=False, required=False)

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def clean(self):
        cleaned_data = super().clean()
        if 'pity' not in cleaned_data or cleaned_data['pity'] == None:
            cleaned_data['pity']= 0
        if 'guaranteed' not in cleaned_data or cleaned_data['guaranteed'] == None:
            cleaned_data['guaranteed'] = False
        return cleaned_data
class AnalyzeStatisticsWeaponToProbabilityForm(forms.Form):
    class Meta:
        fields = ['numwishes', 'pity', 'guaranteed','fate_points']
    numwishes = forms.IntegerField(label="Number of wishes",min_value=0,error_messages={'required': "Please add your number of wishes", 'min_value': "Number of wishes must be greater than 0"})
    pity = forms.IntegerField(label="Pity", max_value=80,min_value=0, initial=0, required=False, error_messages={'min_value': "Pity must be between 0 and 80", 'max_value': "Pity must be between 0 and 80"})
    guaranteed = forms.BooleanField(label="Have Guaranteed", initial=False, required=False)
    fate_points = forms.IntegerField(label="Number of Fate Points", min_value=0,max_value=2,initial=0,required=False, error_messages={'min_value': "Fate Points must be between 0 and 2", 'max_value': "Fate Points must be between 0 and 2"})

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def clean(self):
        cleaned_data = super().clean()
        if 'pity' not in cleaned_data or cleaned_data['pity'] == None:
            cleaned_data['pity']= 0
        if 'guaranteed' not in cleaned_data or  cleaned_data['guaranteed'] == None:
            cleaned_data['guaranteed'] = False
        if 'fate_points' not in cleaned_data or cleaned_data['fate_points'] == None:
            cleaned_data['fate_points']  = 0
        return cleaned_data

class AnalyzeStatisticsCharacterToNumWishesForm(forms.Form):
    class Meta:
        fields = ['numcopies', 'minimum_probability','pity', 'guaranteed']
    numcopies = forms.IntegerField(label="Number of Copies Desired",max_value=7,min_value=1, initial=1,error_messages={'required': "Please add your number of copies desired", 'min_value': "Number of copies must be between 1 and 7", 'max_value': "Number of copies must be between 1 and 7"})
    minimum_probability = forms.FloatField(label="Minimum Probability of Copies Desired",max_value=1,min_value=0, initial=0, error_messages={'required': "Please give the probability desired.", 'min_value': "Probability must be between 0 and 1", 'max_value': "Probability must be between 0 and 1"})
    pity = forms.IntegerField(label="Pity",max_value=90,min_value=0, initial=0, required=False, error_messages={'min_value': "Pity must be between 0 and 90", 'max_value': "Pity must be between 0 and 90"})
    guaranteed = forms.BooleanField(label="Have Guaranteed",initial=False, required=False)

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def clean(self):
        cleaned_data = super().clean()
        if 'pity' not in cleaned_data or cleaned_data['pity'] == None:
            cleaned_data['pity']= 0
        if 'guaranteed' not in cleaned_data or cleaned_data['guaranteed'] == None:
            cleaned_data['guaranteed'] = False
        return cleaned_data
class AnalyzeStatisticsWeaponToNumWishesForm(forms.Form):
    class Meta:
        fields = ['numcopies', 'minimum_probability','pity', 'guaranteed','fate_points']
    numcopies = forms.IntegerField(label="Number of Copies Desired",max_value=5,min_value=1, initial=1, error_messages={'required': "Please add your number of copies desired", 'min_value': "Number of copies must be between 1 and 5", 'max_value': "Number of copies must be between 1 and 5"})
    minimum_probability = forms.FloatField(label="Minimum Probability of Copies Desired",max_value=1,min_value=0, initial=0, error_messages={'required': "Please give the probability desired.", 'min_value': "Probability must be between 0 and 1", 'max_value': "Probability must be between 0 and 1"})
    pity = forms.IntegerField(label="Pity",max_value=80,min_value=0, initial=0, required=False,error_messages={'min_value': "Pity must be between 0 and 80", 'max_value': "Pity must be between 0 and 80"})
    guaranteed = forms.BooleanField(label="Have Guaranteed",initial=False, required=False)
    fate_points = forms.IntegerField(label="Number of Fate Points", min_value=0,max_value=2,initial=0,required=False,error_messages={'min_value': "Fate Points must be between 0 and 2", 'max_value': "Fate Points must be between 0 and 2"})

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def clean(self):
        cleaned_data = super().clean()
        if 'pity' not in cleaned_data or cleaned_data['pity'] == None:
            cleaned_data['pity']= 0
        if 'guaranteed' not in cleaned_data or  cleaned_data['guaranteed'] == None:
            cleaned_data['guaranteed'] = False
        if 'fate_points' not in cleaned_data or cleaned_data['fate_points'] == None:
            cleaned_data['fate_points']  = 0
        return cleaned_data

class ProjectPrimosForm(forms.Form):
    numprimos = forms.IntegerField(label="Number of Wishes",min_value=0,initial=0,error_messages={'min_value': "Please give a positive number of primogems."} )
    numgenesis = forms.IntegerField(label="Number of Genesis Crystal",min_value=0,initial=0,error_messages={'min_value': "Please give a positive number of genesis crystals."})
    numfates = forms.IntegerField(label="Number of Intertwined Fate",min_value=0,initial=0,error_messages={'min_value': "Please give a positive number of intertwined fates"})
    numstarglitter = forms.IntegerField(label="Number of Starglitter",min_value=0,initial=0,error_messages={'min_value': "Please give a positive number of starglitter"})
    end_date_manual_select = forms.DateField(label="End Date Manual Select",widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    # TODO fix this to be less jank if possible
    now = datetime.date.today()
    valid_char_banners = models.CharacterBanner.objects.filter(enddate__gte=now)
    valid_weapon_banners = models.WeaponBanner.objects.filter(enddate__gte=now)
    banner_ids = [banner.get_base_banner_equivalent().id for banner in valid_char_banners]
    banner_ids+= [banner.get_base_banner_equivalent().id for banner in valid_weapon_banners]
    banners = models.Banner.objects.filter(id__in=banner_ids)
    # banners = models.Banner.objects.all()
    end_date_banner_select = forms.ModelChoiceField(label="End Date Select Through Banner",
        queryset= banners,
        widget=forms.Select(attrs={'size': 30},),
        initial=timezone.now(),
         required=False
    )

    welkin_moon = forms.BooleanField(label="Welkin Moon",initial=False, required=False)
    battlepass = forms.BooleanField(label="Battlepass",initial=False, required=False)
    average_abyss_stars = forms.IntegerField(label="Average Abyss Stars",initial=27, required=False)

    def manual_select_is_default(self):
        cleaned_data = super().clean()
        today = datetime.date.today()
        split_date_default = [str(today.year), "01", "01"]
        split_date_manual = str(cleaned_data["end_date_manual_select"]).split("-")
        if split_date_manual == split_date_default:
            return True
        else:
            return False

    def date_is_decidable(self):
        cleaned_data = super().clean()
        # currently only works in an XOR fashion
        if cleaned_data["end_date_banner_select"] == None and self.manual_select_is_default():
            return False
        elif cleaned_data["end_date_banner_select"] != None and self.manual_select_is_default():
            return True
        elif cleaned_data["end_date_banner_select"] == None and not self.manual_select_is_default():
            return True
        elif cleaned_data["end_date_banner_select"] != None and not self.manual_select_is_default():
            return False

    def decide_date(self):
        cleaned_data = super().clean()
        if cleaned_data["end_date_banner_select"]!= None and self.manual_select_is_default():
            specified_banner = cleaned_data["end_date_banner_select"].get_specified_banner_equivalent()
            enddate = specified_banner.enddate
            return enddate
        elif cleaned_data["end_date_banner_select"] == None and not self.manual_select_is_default():
            return cleaned_data["end_date_manual_select"]

    def is_valid(self) -> bool:
        valid = super().is_valid()
        if not self.date_is_decidable():
            return False
        return valid

    def clean(self):
        cleaned_data = super().clean()
        if 'welkin_moon' not in cleaned_data or cleaned_data['welkin_moon'] == None:
            cleaned_data['welkin_moon'] = False
        if 'battlepass' not in cleaned_data or cleaned_data['battlepass'] == None:
            cleaned_data['battlepass'] = False
        if 'average_abyss_stars' not in cleaned_data or cleaned_data['average_abyss_stars'] == None:
            cleaned_data['average_abyss_stars'] = False
            
        return cleaned_data
    
class WishSimulatorForm(forms.Form):
    class Meta:
        fields = ['number_of_pulls', 'banner']
    number_of_pulls = forms.IntegerField(label="Number of Pulls",min_value=1, initial=1)
    banners  = models.Banner.objects.all()
    banner = forms.ModelChoiceField(label="Banner:",
        queryset= banners,
        widget=forms.Select(attrs={'size': 30},),
        initial=timezone.now(),
         required=True
    )

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data