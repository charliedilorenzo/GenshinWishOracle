from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views import View
from django.urls import reverse_lazy

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
        print("HERE", banners[0].rateups)
        # question = get_object_or_404(Question, pk=question_id)
        return banners
    # characters = Character.objects.
    # template_name = 'analyze/index.html'
    # context_object_name = 
    pass

class CharacterBannerCreateView(generic.CreateView):
    model = CharacterBanner
    fields = ('name', 'rateups')
    success_url = reverse_lazy('analyze:characterbanner')
    template_name = 'analyze/characterbannercreate.html'


class WeaponBannerView(generic.TemplateView):
    # TODO
    # template_name = 'analyze/index.html'
    # context_object_name = 
    pass

class StatisticsAnalyzeView(generic.TemplateView):
    # TODO
    pass