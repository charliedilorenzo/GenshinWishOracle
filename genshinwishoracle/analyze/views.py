from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import View
from django.urls import reverse_lazy
from . import forms

from .models import Character, Weapon, CharacterBanner, WeaponBanner


class IndexView(generic.ListView):
    template_name = 'analyze/index.html'
    context_object_name = 'suburls'

    def get_queryset(self):
        list = ["analyze:characterbanner", "analyze:weaponbanner", "analyze:analyzestatistics"]
        return list

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class CharacterBannerView(generic.ListView):
    # TODO
    template_name = 'analyze/characterbanner.html'
    context_object_name = 'character_banners'

    def get_queryset(self):
        banners = CharacterBanner.objects.order_by()
        return banners

class WeaponBannerView(generic.ListView):
    # TODO
    template_name = 'analyze/weaponbanner.html'
    context_object_name = 'weapon_banners'

    def get_queryset(self):
        banners = WeaponBanner.objects.order_by()
        return banners

class CharacterBannerCreateView(generic.CreateView):
    model = CharacterBanner
    form_class = forms.CreateCharacterBannerForm
    template_name = 'analyze/characterbannercreate.html'
    success_url = reverse_lazy('analyze:characterbanner')

class WeaponBannerCreateView(generic.CreateView):
    model = WeaponBanner
    form_class = forms.CreateWeaponBannerForm
    template_name = 'analyze/weaponbannercreate.html'
    success_url = reverse_lazy('analyze:weaponbanner')

class StatisticsAnalyzeView(generic.TemplateView):
    # TODO
    pass