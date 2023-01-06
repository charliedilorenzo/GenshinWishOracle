from django import forms
from . import models
from .validators import validate_character_rateups
from django.utils import timezone

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