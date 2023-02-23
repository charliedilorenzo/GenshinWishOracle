from django import forms
from . import models
from .validators import validate_character_rateups
from django.utils import timezone
import datetime
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from users.models import Profile

# imported from django.contrib.admin
class FilteredSelectMultiple(forms.SelectMultiple):
    """
    A SelectMultiple with a JavaScript filter interface.

    Note that the resulting JavaScript assumes that the jsi18n
    catalog has been loaded in the page
    """

    class Media:
        css = {
                'all': ('/static/admin/css/widgets.css',),
            }
        js = [
            settings.STATIC_URL + "analyze/js/core.js",
            settings.STATIC_URL + "analyze/js/SelectBox.js",
            settings.STATIC_URL + "analyze/js/SelectFilter2.js",
            '/jsi18n',
        ]

    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        self.verbose_name = verbose_name
        self.is_stacked = is_stacked
        super().__init__(attrs, choices)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["attrs"]["class"] = "selectfilter"
        if self.is_stacked:
            context["widget"]["attrs"]["class"] += "stacked"
        context["widget"]["attrs"]["data-field-name"] = self.verbose_name
        context["widget"]["attrs"]["data-is-stacked"] = int(self.is_stacked)
        return context


class CreateCharacterBannerForm(forms.ModelForm):
    class Meta:
        model = models.CharacterBanner
        fields = ['name', 'rateups', 'enddate']
    name = forms.CharField(max_length = 64,error_messages={'required': "Please add a banner name."})
    custom_widget = FilteredSelectMultiple('rateups', is_stacked=False)
    rateups = forms.ModelMultipleChoiceField(
        queryset=models.Character.objects.all(),
        widget=custom_widget,
        required = True, 
        error_messages={'required': "Please add rateups to the banner."},
        label = "Rateup"
    )
    enddate = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))

    def verify_rateups(self):
        cleaned_data = super().clean()
        rateups = cleaned_data.get('rateups')
        if rateups is None or len(rateups) == 0:
            return False
        rateups_breakdown = {}
        rateup_reqs = self.get_rateup_requirements()
        for key in rateup_reqs:
            rateups_breakdown[key] = len(rateups.filter(rarity=key))
        if rateups_breakdown == rateup_reqs:
            return True
        return False

    def is_valid(self) -> bool:
        valid = super().is_valid()
        if not self.verify_rateups():
            return False
        return valid

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def get_rateup_requirements(self) -> dict[int:int]:
        rateup_reqs = {3: 0, 4: 3, 5: 1}
        return rateup_reqs
    
    def save(self, commit=True) -> models.CharacterBanner:
        cleaned_data = super().clean()
        # if not commit:
        #     raise NotImplementedError("Can't create object without database save")
        rateups = cleaned_data.get('rateups')
        kwargs = {'name': cleaned_data.get('name'), 'enddate': cleaned_data.get('enddate')}
        character_banner = self.Meta.model(**kwargs)
        character_banner.save()    
        character_banner.rateups.set(rateups)
        return character_banner

class CreateWeaponBannerForm(forms.ModelForm):
    class Media:
        js = ("my_code.js",)
    class Meta:
        model = models.WeaponBanner
        fields = ['name', 'rateups', 'enddate']
    name = forms.CharField(max_length = 64, error_messages={'required': "Please add a banner name."})
    custom_widget = FilteredSelectMultiple('rateups', is_stacked=False)
    rateups = forms.ModelMultipleChoiceField(
        queryset=models.Weapon.objects.filter(~Q(rarity = 3)),
        widget=custom_widget,
        error_messages={'required': "Please add rateups to the banner."}
    )
    enddate = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))

    def verify_rateups(self):
        cleaned_data = super().clean()
        rateups = cleaned_data.get('rateups')
        if rateups is None or len(rateups) == 0:
            return False
        rateups_breakdown = {}
        rateup_reqs = self.get_rateup_requirements()
        for key in rateup_reqs:
            rateups_breakdown[key] = len(rateups.filter(rarity=key))
        if rateups_breakdown == rateup_reqs:
            return True
        return False
    
    def is_valid(self) -> bool:
        valid = super().is_valid()
        if not self.verify_rateups():
            return False
        return valid

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def get_rateup_requirements(self) -> dict[int:int]:
        rateup_reqs = {3: 0, 4: 5, 5: 2}
        return rateup_reqs
    
    def save(self, commit=True) -> models.WeaponBanner:
        cleaned_data = super().clean()
        # if not commit:
        #     raise NotImplementedError("Can't create object without database save")
        rateups = cleaned_data.get('rateups')
        kwargs = {'name': cleaned_data.get('name'), 'enddate': cleaned_data.get('enddate')}
        weapon_banner = self.Meta.model(**kwargs)
        weapon_banner.save()    
        weapon_banner.rateups.set(rateups)
        return weapon_banner

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
    class Meta:
        fields = ['numprimos', 'numgenesis', 'numfates', 'numstarglitter', 'end_date_manual_select', 'end_date_banner_select', 'welkin_moon', 'battlepass', 'average_abyss_stars']\

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(ProjectPrimosForm, self).__init__(*args, **kwargs)
        self.fields['numprimos'] = forms.IntegerField(label="Number of Wishes",min_value=0,initial=0,error_messages={'min_value': "Please give a positive number of primogems."} )
        self.fields['numgenesis'] = forms.IntegerField(label="Number of Genesis Crystal",min_value=0,initial=0,error_messages={'min_value': "Please give a positive number of genesis crystals."})
        self.fields['numfates'] = forms.IntegerField(label="Number of Intertwined Fate",min_value=0,initial=0,error_messages={'min_value': "Please give a positive number of intertwined fates"})
        self.fields['numstarglitter'] = forms.IntegerField(label="Number of Starglitter",min_value=0,initial=0,error_messages={'min_value': "Please give a positive number of starglitter"})
        self.fields['end_date_manual_select'] = forms.DateField(label="End Date Manual Select",widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")))

        self.fields['welkin_moon'] = forms.BooleanField(label="Welkin Moon",initial=False, required=False)
        self.fields['battlepass '] = forms.BooleanField(label="Battlepass",initial=False, required=False)
        self.fields['average_abyss_stars'] = forms.IntegerField(label="Average Abyss Stars",initial=27, required=False)
        if user_id is not None:
            user = User.objects.filter(id=user_id)
        else:
            user = User.objects.none()
        # check they actually exist
        if len(user) != 1:
            pass
        else:
            profile = Profile.objects.filter(user_id=user_id)
            if len(profile) != 1:
                return 
            profile = profile[0]
            now = datetime.date.today()
            banners = profile.banners.filter(enddate__gte=now)
            self.fields['end_date_banner_select '] = forms.ModelChoiceField(label="End Date Select Through Banner",
                queryset= banners,
                widget=forms.Select(attrs={'size': 30},),
                initial=timezone.now(),
                required=False
            )

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
     # TODO fix it 
    banners = models.Banner.objects.all()

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