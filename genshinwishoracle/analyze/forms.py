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

class AnalyzeStatisticsCharacterForm(forms.Form):
    numwishes = forms.IntegerField(min_value=0)
    pity = forms.IntegerField(max_value=90,min_value=0, initial=0, required=False)
    guaranteed = forms.BooleanField(initial=False, required=False)

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['pity'] == None:
            cleaned_data['pity']= 0
        if cleaned_data['guaranteed'] == None:
            cleaned_data['guaranteed'] = False
        return cleaned_data
class AnalyzeStatisticsWeaponForm(forms.Form):
    numwishes = forms.IntegerField(min_value=0)
    pity = forms.IntegerField(max_value=80,min_value=0, initial=0, required=False)
    guaranteed = forms.BooleanField(initial=False, required=False)
    fate_points = forms.IntegerField(min_value=0,max_value=2,initial=0,required=False)

    def is_valid(self) -> bool:
        valid = super().is_valid()
        return valid

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['pity'] == None:
            cleaned_data['pity']= 0
        if cleaned_data['guaranteed'] == None:
            cleaned_data['guaranteed'] = False
        if cleaned_data['fate_points'] == None:
            cleaned_data['fate_points']  = 0
        return cleaned_data

class ProjectPrimosForm(forms.Form):
    numprimos = forms.IntegerField(min_value=0,initial=0,required=True)
    numgenesis = forms.IntegerField(min_value=0,initial=0,required=True)
    numfates = forms.IntegerField(min_value=0,initial=0,required=True)
    numstarglitter = forms.IntegerField(min_value=0,initial=0,required=True)
    end_date_manual_select = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))
    end_date_banner_select = forms.ModelChoiceField(
        queryset= models.Banner.objects.all(),
        widget=forms.Select(attrs={'size': 30},),
        initial=timezone.now(),
         required=False
    )

    welkin_moon = forms.BooleanField(initial=False, required=False)
    battlepass = forms.BooleanField(initial=False, required=False)
    average_abyss_stars = forms.IntegerField(initial=27, required=False)

    def manual_select_is_default(self):
        cleaned_data = super().clean()
        today = datetime.date.today()
        split_date_default = [str(today.year), "01", "01"]

        banner_date =cleaned_data["end_date_banner_select"]
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
            return cleaned_data["end_date_banner_select"]
        elif cleaned_data["end_date_banner_select"] == None and not self.manual_select_is_default():
            return cleaned_data["end_date_manual_select"]

    def is_valid(self) -> bool:
        valid = super().is_valid()
        if not self.date_is_decidable():
            return False
        return valid

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data