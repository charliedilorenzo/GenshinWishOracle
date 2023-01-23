from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
from django.views import generic
from django.urls import reverse_lazy
from . import forms
from django.urls import reverse

from .models import Character, Weapon, CharacterBanner, WeaponBanner

from .analytical import AnalyticalCharacter, AnalyticalWeapon

class IndexView(generic.ListView):
    template_name = 'analyze/index.html'
    context_object_name = 'index'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        list = []
        return list

class CharacterBannerView(generic.ListView):
    template_name = 'analyze/characterbanner.html'
    context_object_name = 'character_banners'

    def get_queryset(self):
        banners = CharacterBanner.objects.order_by()
        return banners

class WeaponBannerView(generic.ListView):
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

class StatisticsAnalyzeCharacterView(generic.FormView):
    form_class = forms.AnalyzeStatisticsCharacterForm
    template_name = 'analyze/analyze_statistics_character.html'
    success_url = reverse_lazy('analyze:analyzestatisticsresults')
class StatisticsAnalyzeWeaponView(generic.FormView):
    form_class = forms.AnalyzeStatisticsWeaponForm
    template_name = 'analyze/analyze_statistics_weapon.html'
    success_url = reverse_lazy('analyze:analyzestatisticsresults')

class StatisticsResultView(generic.View):
    template_name = 'analyze/analyze_result.html'
    success_url = reverse_lazy('analyze:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data

def switch_banner_type_character(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = forms.AnalyzeStatisticsCharacterForm
        if request.POST.get("select_weapon_banner"):
            form = forms.AnalyzeStatisticsWeaponForm()
            return render(request, 'analyze/analyze_statistics_weapon.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.AnalyzeStatisticsCharacterForm()
    return render(request, 'analyze/analyze_statistics_character.html', {'form': form})

def switch_banner_type_weapon(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = forms.AnalyzeStatisticsWeaponForm
        if request.POST.get("select_character_banner"):
            form = forms.AnalyzeStatisticsCharacterForm()
            return render(request, 'analyze/analyze_statistics_chararcter.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.AnalyzeStatisticsWeaponForm()
    return render(request, 'analyze/analyze_statistics_weapon.html', {'form': form})

def analysis_in_progress(request):
        if request.method == 'POST':
            #just do this to check the type
            if 'character_banner_submit' in request.POST:
                banner_type = "character"
            elif 'weapon_banner_submit' in request.POST:
                banner_type = "weapon"
            else:
                return render(request, 'analyze/analyze_result.html')
            if banner_type == "character":
                form  = forms.AnalyzeStatisticsCharacterForm(request.POST)
                if form.is_valid():
                    print("Valid character banner")
                    cleaned = form.cleaned_data
                    numwishes = cleaned['numwishes']
                    pity = cleaned['pity']
                    guaranteed = cleaned['guaranteed']

                    analyze_obj = AnalyticalCharacter()
                    solution = analyze_obj.specific_solution(numwishes,pity,guaranteed,0)
                    place_values = 3 
                    for key in solution:
                        print(float(solution[key]))
                        print("%.3f" % float(solution[key]))
                        print(("%.{}f".format(place_values) % float(solution[key])))
                        solution[key] = ("%.{}f".format(place_values) % float(solution[key]))
                    print(solution)

                    context = {
                        'banner_type' : banner_type,
                        'X' : solution[0],
                        'C0' : solution[1],
                        'C1' : solution[2],
                        'C2' : solution[3],
                        'C3' : solution[4],
                        'C4' : solution[5],
                        'C5' : solution[6],
                        'C6' : solution[7]
                    }
            elif banner_type == "weapon":
                form  = forms.AnalyzeStatisticsWeaponForm(request.POST)
                if form.is_valid():
                    print("Valid weapon banner")
                    cleaned = form.cleaned_data
                    numwishes = cleaned['numwishes']
                    pity = cleaned['pity']
                    guaranteed = cleaned['guaranteed']
                    fate_points = cleaned['fate_points']

                    analyze_obj = AnalyticalWeapon()
                    solution = analyze_obj.specific_solution(numwishes,pity,guaranteed,fate_points,0)
                    place_values = 3
                    for key in solution:
                        solution[key] = ("%.{}f".format(place_values) % float(solution[key]))

                    context = {
                        'banner_type' : banner_type,
                        'X' : solution[0],
                        'R1' : solution[1],
                        'R2' : solution[2],
                        'R3' : solution[3],
                        'R4' : solution[4],
                        'R5' : solution[5]
                    }
            return render(request, 'analyze/analyze_result.html', context)
        else:
            return render(request, 'analyze/analyze_result.html')