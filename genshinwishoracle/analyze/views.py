from django.shortcuts import get_object_or_404, render, redirect
import datetime

# from django.urls import reverse
from django.views import generic
from django.urls import reverse_lazy
from . import forms
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
import math
from django.contrib.auth.decorators import login_required
from .models import Character, Weapon, CharacterBanner, WeaponBanner

from .analytical import AnalyticalCharacter, AnalyticalWeapon
from .project_primos import project_future_primos
from users.models import Profile
from django.http import HttpResponseRedirect

class IndexView(generic.ListView):
    template_name = 'analyze/index.html'
    context_object_name = 'index'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        list = []
        return list

class CharacterBannerView(generic.ListView):
    template_name = 'analyze/character_banner.html'
    context_object_name = 'character_banners'

    def get_queryset(self):
        banners = CharacterBanner.objects.order_by()
        return banners

class WeaponBannerView(generic.ListView):
    template_name = 'analyze/weapon_banner.html'
    context_object_name = 'weapon_banners'

    def get_queryset(self):
        banners = WeaponBanner.objects.order_by()
        return banners

class CharacterBannerCreateView(generic.CreateView):
    model = CharacterBanner
    form_class = forms.CreateCharacterBannerForm
    template_name = 'analyze/character_banner_create.html'
    success_url = reverse_lazy('analyze:character_banner')

class WeaponBannerCreateView(generic.CreateView):
    model = WeaponBanner
    form_class = forms.CreateWeaponBannerForm
    template_name = 'analyze/weapon_banner_create.html'
    success_url = reverse_lazy('analyze:weapon_banner')

class StatisticsAnalyzeCharacterView(generic.FormView):
    form_class = forms.AnalyzeStatisticsCharacterForm
    template_name = 'analyze/analyze_statistics_character.html'
    success_url = reverse_lazy('analyze:analyze_results')
    def get(self, request, *args, **kwargs):
        if 'input_user_data_character' in request.session and request.session['input_user_data_character'] == True:
            print(request.session['input_user_data_character'])
            if request.user.is_authenticated:
                curr_user_prof = Profile.objects.filter(user_id = request.user.id)[0]
                wishes = math.floor(curr_user_prof.calculate_pure_primos()/160)
                init = {'numwishes':wishes,'pity':curr_user_prof.character_pity,'guaranteed': curr_user_prof.character_guaranteed }
                form = self.form_class(initial=init)
                request.session["input_user_data_character"] = False
                return render(request, self.template_name, context={'form': form})
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        # check if we pressed the switch button 
        if request.POST.get("select_weapon_banner"):
            return redirect(to='/analyze/statistics/weapon/')
        # i dont want to include extra stuff in the url personally
        # still need to redirect though to allow update form
        # redirect for self and add a session flag to alter initial form data
        if request.POST.get("import_user_data_character"):
            if request.user.is_authenticated:
                request.session["input_user_data_character"] = True
                return redirect(to='/analyze/statistics/character/')
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            numwishes = cleaned['numwishes']
            pity = cleaned['pity']
            guaranteed = cleaned['guaranteed']

            analyze_obj = AnalyticalCharacter()
            solution = analyze_obj.specific_solution(numwishes,pity,guaranteed,0)
            # by 600 misses 5% of values by 700 misses 70%
            place_values = 3 
            for key in solution:
                solution[key] = ("%.{}f".format(place_values) % float(solution[key]))

            context = {
                'banner_type' : "character",
                'X' : solution[0],
                'C0' : solution[1],
                'C1' : solution[2],
                'C2' : solution[3],
                'C3' : solution[4],
                'C4' : solution[5],
                'C5' : solution[6],
                'C6' : solution[7]
            }
            return render(request, 'analyze/analyze_results.html', context)
        return render(request, self.template_name, {'form': form})


class StatisticsAnalyzeWeaponView(generic.FormView):
    form_class = forms.AnalyzeStatisticsWeaponForm
    template_name = 'analyze/analyze_statistics_weapon.html'
    success_url = reverse_lazy('analyze:analyze_results')
    def get(self, request, *args, **kwargs):
        if 'input_user_data_weapon' in request.session and request.session['input_user_data_weapon'] == True:
            print(request.session['input_user_data_weapon'])
            if request.user.is_authenticated:
                curr_user_prof = Profile.objects.filter(user_id = request.user.id)[0]
                wishes = math.floor(curr_user_prof.calculate_pure_primos()/160)
                init = {'numwishes':wishes,'pity':curr_user_prof.weapon_pity,'guaranteed': curr_user_prof.weapon_guaranteed, 'fate_points': curr_user_prof.weapon_fate_points }
                form = self.form_class(initial=init)
                request.session["input_user_data_weapon"] = False
                return render(request, self.template_name, context={'form': form})
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # check if we pressed the switch button
        if request.POST.get("select_character_banner"):
            return redirect(to='/analyze/statistics/character/')
        # i dont want to include extra stuff in the url personally
        # still need to redirect though to allow update form
        # redirect for self and add a session flag to alter initial form data
        if request.POST.get("import_user_data_character"):
            if request.user.is_authenticated:
                request.session["input_user_data_weapon"] = True
                return redirect(to='/analyze/statistics/weapon/')
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            numwishes = cleaned['numwishes']
            pity = cleaned['pity']
            guaranteed = cleaned['guaranteed']
            fate_points = cleaned['fate_points']

            analyze_obj = AnalyticalWeapon()
            solution = analyze_obj.specific_solution(numwishes,pity,guaranteed,fate_points,0)
            # by 400 deteriorates to missing around 14% of the values
            place_values = 3
            for key in solution:
                solution[key] = ("%.{}f".format(place_values) % float(solution[key]))

            context = {
                'banner_type' : "weapon",
                'X' : solution[0],
                'R1' : solution[1],
                'R2' : solution[2],
                'R3' : solution[3],
                'R4' : solution[4],
                'R5' : solution[5]
            }
            return render(request, 'analyze/analyze_results.html', context)
        return render(request, self.template_name, {'form': form})
class StatisticsResultView(generic.View):
    template_name = 'analyze/analyze_results.html'
    success_url = reverse_lazy('analyze:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data
class ProjectPrimosView(generic.FormView):
    template_name = 'analyze/project_primos.html'
    success_url = reverse_lazy('analyze:project_primos_results')
    form_class = forms.ProjectPrimosForm

def project_primos_in_progress(request):
        if request.method == 'POST':
            form  = forms.ProjectPrimosForm(request.POST)
            if form.is_valid():
                cleaned = form.cleaned_data
                if form.date_is_decidable() == False:
                    return render(request, 'analyze/project_primos.html')

                future_date = form.decide_date()
                now = datetime.date.today()
                days_until_enddate = (future_date-now).days
                if days_until_enddate < 0:
                    # non-sensical end date
                    return render(request, 'analyze/project_primos.html')
                current_date = timezone.now
                pure_primo_estimate = cleaned['numprimos']+cleaned['numgenesis']+160*math.floor(cleaned['numstarglitter']/5)+ 160*cleaned['numfates']
                current_primos = pure_primo_estimate

                future_primos = project_future_primos(current_primos, 0,0,0,days_until_enddate,cleaned['welkin_moon'],cleaned['battlepass'], cleaned['average_abyss_stars'])
                current_wishes = math.floor(current_primos/160)
                future_wishes = math.floor(future_primos/160)
                context = {
                    'current_primos': current_primos,
                    'future_primos': future_primos,
                    'current_wishes': current_wishes,
                    'future_wishes': future_wishes,
                    'current_date': current_date,
                    'future_date': future_date
                }
                return render(request, 'analyze/project_primos_result.html', context)
            else:
                return render(request, 'analyze/project_primos.html')
        else:
            return render(request, 'analyze/project_primos_result.html')
class ProjectPrimosResultsView(generic.View):
    template_name = 'analyze/project_primos_results.html'
    success_url = reverse_lazy('analyze:project_primos')
    def get(self, request):
        return render(request, 'analyze/project_primos_results.html')
class ProbabilityToWishesView(generic.View):
    template_name = 'analyze/probability_to_wishes.html'
    success_url = reverse_lazy('analyze:index')
    def get(self, request):
        return render(request, 'analyze/probability_to_wishes.html')

class WishSimulatorView(generic.View):
    template_name = 'analyze/wish_simulator.html'
    success_url = reverse_lazy('analyze:index')
    def get(self, request):
       return render(request, 'analyze/wish_simulator.html')