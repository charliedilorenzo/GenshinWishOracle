from django.shortcuts import get_object_or_404, render, redirect
import datetime

# from django.urls import reverse
from django.views import generic
from django.urls import reverse_lazy
from . import forms
from django.urls import reverse
from django.utils import timezone
import math
from django.contrib.auth.decorators import login_required
from .models import CharacterBanner, WeaponBanner

from .analytical import AnalyticalCharacter, AnalyticalWeapon
from .project_primos import project_future_primos
from users.models import Profile
from . import utils

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

class StatisticsAnalyzeOmniView(generic.View):
    template_name = 'analyze/analyze_omni.html'
    result_template = 'analyze/analyze_results.html'
    valid_banner_types = ['character', 'weapon']
    valid_statistics_types = ['calcprobability', 'calcnumwishes']
    default_url = "/analyze/{}/{}/".format(valid_banner_types[0], valid_statistics_types[0])

    def get(self, request,banner_type, statistics_type, *args, **kwargs):
        if banner_type not in self.valid_banner_types or statistics_type not in self.valid_statistics_types:
            return redirect(to=self.default_url)
        context = {"banner_type":banner_type,"statistics_type": statistics_type }
        first_form = self.get_first_form(request,banner_type=banner_type,statistics_type=statistics_type)
        request.session['import_data'] = False
        context["first_form"] = first_form
        second_form_names =  self.get_second_form_names(request,banner_type=banner_type,statistics_type=statistics_type,first_form=first_form)
        context["second_form_names"] = second_form_names

        return render(request, self.template_name, context=context)

    def get_first_form(self, request, banner_type, statistics_type):
        init = {}
        form = self.banner_statistics_combo_to_form_obj(banner_type, statistics_type)
        if request.POST:
            request.session['wishes'] = None
            form = form(request.POST)
            return form
        elif 'import_data' in request.session and request.session['import_data'] == True:
            if request.user.is_authenticated:
                curr_user_prof = Profile.objects.filter(user_id = request.user.id)[0]
                wishes = math.floor(curr_user_prof.calculate_pure_primos()/160)
                if banner_type == "character":
                    init.update({'numwishes':wishes,'pity':curr_user_prof.character_pity,'guaranteed': curr_user_prof.character_guaranteed })
                elif banner_type == "weapon":
                    init = {'numwishes':wishes,'pity':curr_user_prof.weapon_pity,'guaranteed': curr_user_prof.weapon_guaranteed, 'fate_points': curr_user_prof.weapon_fate_points }
        # not very elegant but alternatives also seems to suck
        elif 'wishes' in request.session and not request.session['wishes'] == None:
            init.update({'numwishes': request.session['wishes']})
        form = form(initial=init)
        return form
        # if statistics_type == "calcprobability" and banner_type == "character":
        #     form = forms.AnalyzeStatisticsCharacterToProbabilityForm(initial=init)
        # elif statistics_type == "calcprobability" and banner_type == "weapon":
        #     form = forms.AnalyzeStatisticsWeaponToProbabilityForm(initial=init)
        # elif statistics_type == "calcnumwishes" and banner_type == "character":
        #     form = forms.AnalyzeStatisticsCharacterToNumWishesForm(initial=init)
        # elif statistics_type == "calcnumwishes" and banner_type == "weapon":
        #     form = forms.AnalyzeStatisticsWeaponToNumWishesForm(initial=init)
    
    def get_second_form_names(self, request, banner_type, statistics_type,first_form):
        if statistics_type == "calcprobability" and banner_type == "character":
            form = forms.AnalyzeStatisticsCharacterToNumWishesForm
        elif statistics_type == "calcprobability" and banner_type == "weapon":
            form = forms.AnalyzeStatisticsWeaponToNumWishesForm
        elif statistics_type == "calcnumwishes" and banner_type == "character":
            form = forms.AnalyzeStatisticsCharacterToProbabilityForm
        elif statistics_type == "calcnumwishes" and banner_type == "weapon":
            form = forms.AnalyzeStatisticsWeaponToProbabilityForm
        # technically could just remove pity/guaranteed/fate_points
        names = []
        for field in form.Meta.fields:
            if field not in first_form.Meta.fields:
                names.append(field)
        return names

    def  banner_statistics_combo_to_form_obj(self,banner_type, statistics_type):
        if statistics_type == "calcprobability" and banner_type == "character":
            form = forms.AnalyzeStatisticsCharacterToProbabilityForm
        elif statistics_type == "calcprobability" and banner_type == "weapon":
            form = forms.AnalyzeStatisticsWeaponToProbabilityForm
        elif statistics_type == "calcnumwishes" and banner_type == "character":
            form = forms.AnalyzeStatisticsCharacterToNumWishesForm
        elif statistics_type == "calcnumwishes" and banner_type == "weapon":
            form = forms.AnalyzeStatisticsWeaponToNumWishesForm
        return form

    def post(self, request, banner_type, statistics_type,*args, **kwargs):
        context = {}
        # check if we pressed the switch button
        redirect_buttons = self.button_name_post_to_redirect(request, banner_type, statistics_type)
        if not redirect_buttons is None:
            return redirect_buttons
        # i dont want to include extra stuff in the url personally
        # still need to redirect though to allow update form
        # redirect for self and add a session flag to alter initial form data
        if request.POST.get("import_user_data"):
            if request.user.is_authenticated:
                request.session["import_data"] = True
                return redirect(to=reverse('analyze:statistics', kwargs={"banner_type":banner_type, "statistics_type":statistics_type}))
        elif request.POST.get("reset_values"):
            request.session.pop('wishes')
            request.session['import_data'] = False
            context = {"banner_type":banner_type,"statistics_type": statistics_type }
            first_form = self.get_first_form(request,banner_type=banner_type,statistics_type=statistics_type)
            context["first_form"] = first_form
            second_form_names =  self.get_second_form_names(request,banner_type=banner_type,statistics_type=statistics_type,first_form=first_form)
            context["second_form_names"] = second_form_names
            return render(request, self.template_name, context=context)
        if request.POST.get("reset"):
            if 'wishes' in request.session:
                request.session.pop('wishes')
        request.session['import_data'] = False
        # add request post to the correct type given by function
        form = self.get_first_form(request,banner_type,statistics_type)
        if form.is_valid():
            cleaned = form.cleaned_data
            place_values = 3 
            if banner_type == "character" and statistics_type == "calcprobability":
                analyze_obj = AnalyticalCharacter()
                solution = analyze_obj.specific_solution(cleaned['numwishes'],cleaned['pity'],cleaned['guaranteed'],0)
                for key in solution:
                    solution[key] = ("%.{}f".format(place_values) % float(solution[key]))
                context = {
                    'banner_type' : banner_type.capitalize(),
                    'statistics_type': statistics_type,
                    'X' : solution[0],
                    'C0' : solution[1],
                    'C1' : solution[2],
                    'C2' : solution[3],
                    'C3' : solution[4],
                    'C4' : solution[5],
                    'C5' : solution[6],
                    'C6' : solution[7],
                    'pity': cleaned['pity'],
                    'guaranteed': cleaned['guaranteed'],
                    'numwishes': cleaned['numwishes']
                }


                # width = 0.35
                # pyplot.switch_backend('AGG')
                # ind = numpy.arange(len(solution.keys())) # the x locations for the groups
                # fig = pyplot.figure(figsize=(10, 4))
                # # ax = fig.add_axes([0,0,1,1])
                # # ax.bar(ind, values, width)
                # pyplot.bar(numpy.arange(len(keys)) , values, width)
                # # ax.set_ylabel('Portion')
                # # guaranteed_text = "with" if cleaned['guaranteed'] else "without"
                # # ax.set_title('Wish Probability Breakdown for: {} Wishes, {} Pity, {} Guaranteed'.format(cleaned['numwishes'], cleaned['pity'], guaranteed_text))
                # # ax.set_xticks(ind, ('G0','G1', 'G2', 'G3', 'G4', 'G5','G6','G7'))
                # # ax.set_yticks(numpy.arange(0, 1, .1))
                # guaranteed_text = "with" if cleaned['guaranteed'] else "without"
                # pyplot.ylabel('Portion Resuling in Specified Constellation')
                # pyplot.title('Wish Probability Breakdown for: {} Wishes, {} Pity, {} Guaranteed'.format(cleaned['numwishes'], cleaned['pity'], guaranteed_text))
                # x_labels = ('E0','E1', 'E2', 'E3', 'E4', 'E5','E6','E7')
                # if banner_type == "character":
                #     x_labels = ["X"]
                #     for i in range(0,7):
                #         x_labels.append("C"+str(i))
                # elif banner_type == "weapon":
                #     x_labels = ["X"]
                #     for i in range(1,6):
                #         x_labels.append("C"+str(i))
                # pyplot.xticks(ind, x_labels)
                # pyplot.yticks(numpy.arange(0, 1, .1))
                # pyplot.tight_layout()
                # buffer = BytesIO()
                # pyplot.savefig(buffer, format='png')
                # buffer.seek(0)
                # image_png = buffer.getvalue()
                # graph = base64.b64encode(image_png)
                # graph = graph.decode('utf-8')
                # buffer.close()
                context['chart'] = utils.bar_graph_for_statistics(solution,banner_type, statistics_type, cleaned['numwishes'],cleaned['pity'],cleaned['guaranteed'],0)
            elif banner_type == "weapon" and statistics_type == "calcprobability":
                analyze_obj = AnalyticalWeapon()
                solution = analyze_obj.specific_solution(cleaned['numwishes'],cleaned['pity'],cleaned['guaranteed'],cleaned['fate_points'],0)
                # by 400 deteriorates to missing around 14% of the values
                place_values = 3
                for key in solution:
                    solution[key] = ("%.{}f".format(place_values) % float(solution[key]))
                context = {
                    'banner_type' : banner_type.capitalize(),
                    'statistics_type': statistics_type,
                    'X' : solution[0],
                    'R1' : solution[1],
                    'R2' : solution[2],
                    'R3' : solution[3],
                    'R4' : solution[4],
                    'R5' : solution[5],
                    'pity': cleaned['pity'],
                    'guaranteed': cleaned['guaranteed'],
                    'fate_points': cleaned['fate_points'],
                    'numwishes': cleaned['numwishes']
                }
                context['chart'] = utils.bar_graph_for_statistics(solution,banner_type, statistics_type, cleaned['numwishes'],cleaned['pity'],cleaned['guaranteed'],cleaned['fate_points'])
            elif banner_type == "character" and statistics_type == "calcnumwishes":
                analyze_obj = AnalyticalCharacter()
                numwishes = analyze_obj.probability_on_copies_to_num_wishes(cleaned['minimum_probability'], cleaned['numcopies'],cleaned['pity'], cleaned['guaranteed'])
                context = {
                    'banner_type' : banner_type.capitalize(),
                    'statistics_type': statistics_type,
                    'numwishes': numwishes,
                    'probability': cleaned['minimum_probability'],
                    'numcopies': cleaned['numcopies'],
                    'pity': cleaned['pity'],
                    'guaranteed': cleaned['guaranteed']
                }
                chart = ""
            elif banner_type == "weapon" and statistics_type == "calcnumwishes":
                analyze_obj = AnalyticalWeapon()
                numwishes = analyze_obj.probability_on_copies_to_num_wishes(cleaned['minimum_probability'], cleaned['numcopies'],cleaned['pity'], cleaned['guaranteed'],cleaned['fate_points'])
                context = {
                    'banner_type' : banner_type.capitalize(),
                    'statistics_type': statistics_type,
                    'numwishes': numwishes,
                    'probability': cleaned['minimum_probability'],
                    'numcopies': cleaned['numcopies'],
                    'pity': cleaned['pity'],
                    'guaranteed': cleaned['guaranteed'],
                    'fate_points': cleaned['fate_points']
                }
            return render(request, self.result_template, context)
        request.session.pop('wishes')
        request.session['import_data'] = False
        context = {"banner_type":banner_type,"statistics_type": statistics_type }
        first_form = self.get_first_form(request,banner_type=banner_type,statistics_type=statistics_type)
        context["first_form"] = first_form
        second_form_names =  self.get_second_form_names(request,banner_type=banner_type,statistics_type=statistics_type,first_form=first_form)
        context["second_form_names"] = second_form_names
        return render(request, self.template_name, context)

    def button_name_post_to_redirect(self, request, banner_type, statistics_type):
        if request.POST.get("select_weapon_banner"):
            return redirect(to='/analyze/statistics/weapon/{}/'.format(statistics_type))
        elif request.POST.get("select_character_banner"):
            return redirect(to='/analyze/statistics/character/{}/'.format(statistics_type))
        if request.POST.get("select_calcnumwishes"):
            return redirect(to='/analyze/statistics/{}/calcnumwishes/'.format(banner_type))
        elif request.POST.get("select_calcprobability"):
            return redirect(to='/analyze/statistics/{}/calcprobability/'.format(banner_type))
        else:
            return None
class StatisticsResultView(generic.View):
    template_name = 'analyze/analyze_results.html'
    success_url = reverse_lazy('analyze:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data
        
class ProjectPrimosView(generic.FormView):
    template_name = 'analyze/project_primos.html'
    result_template = 'analyze/project_primos_result.html'
    success_url = reverse_lazy('analyze:project_primos_results')
    form_class = forms.ProjectPrimosForm

    def get(self, request,*args, **kwargs):
        context = {}
        # using sessions here since I prefer a flag on the user rather than making the url look worse personally
        if 'import_data' in request.session and request.session['import_data'] == True:
            request.session['import_data'] = False
            if request.user.is_authenticated:
                curr_user_prof = Profile.objects.filter(user_id = request.user.id)[0]
                request.session['import_data'] = False
                init = {'numprimos': curr_user_prof.numprimos, 'numgenesis': curr_user_prof.numgenesis, 'numfates': curr_user_prof.numfates, 'numstarglitter': curr_user_prof.numstarglitter}
                context['form'] = self.form_class(initial=init)
        else:
            context['form'] = self.form_class

        return render(request, self.template_name, context=context)

    def post(self, request,*args, **kwargs):
        context ={}
        if request.POST.get("import_user_data"):
            if request.user.is_authenticated:
                request.session["import_data"] = True
                return redirect(to=reverse_lazy('analyze:project_primos'))
        elif request.POST.get("reset_values"):
            form  = forms.ProjectPrimosForm()
            context['form'] = form
            return render(request, 'analyze/project_primos.html', context=context)
        elif request.POST.get("analyze_with_future_primogems"):
            request.session["wishes"] = request.POST.get("analyze_with_future_primogems")
            banner_type = "character"
            statistics_type = "calcprobability"
            return redirect(to=reverse('analyze:statistics', kwargs={"banner_type":banner_type, "statistics_type":statistics_type}))
        form  = forms.ProjectPrimosForm(request.POST)
        if form.is_valid():
            # using sessions again to allow setiting 
            cleaned = form.cleaned_data
            if form.date_is_decidable() == False:
                return render(request,  self.template_name, context=context)

            future_date = form.decide_date()
            now = datetime.date.today()
            days_until_enddate = (future_date-now).days
            if days_until_enddate < 0:
                # non-sensical end date
                return render(request, self.template_name)
            current_date = timezone.now
            pure_primo_estimate = cleaned['numprimos']+cleaned['numgenesis']+160*math.floor(cleaned['numstarglitter']/5)+ 160*cleaned['numfates']
            current_primos = pure_primo_estimate

            future_primos = project_future_primos(current_primos, 0,0,0,days_until_enddate,cleaned['welkin_moon'],cleaned['battlepass'], cleaned['average_abyss_stars'])
            current_wishes = math.floor(current_primos/160)
            future_wishes = math.floor(future_primos/160)
            context.update({
                'current_primos': current_primos,
                'future_primos': future_primos,
                'current_wishes': current_wishes,
                'future_wishes': future_wishes,
                'current_date': current_date,
                'future_date': future_date})
            return render(request, self.result_template, context=context)
        else:
            context['form'] = form
            return render(request, self.template_name, context=context)
class WishSimulatorView(generic.View):
    template_name = 'analyze/wish_simulator.html'
    success_url = reverse_lazy('analyze:index')
    def get(self, request):
       return render(request, 'analyze/wish_simulator.html')

def context_from_request(request):
    # i couldnt seem to find if there already existed a function for this online 
    list_from_body = request.body.decode().split("&")
    dict_from_body = {}
    for item in list_from_body:
        temp_split = item.split("=")
        dict_from_body[temp_split[0]] = temp_split[1]
    return dict_from_body

def update_session_data(request):
    pass