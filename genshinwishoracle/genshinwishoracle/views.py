from django.views import generic
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
import math
import datetime

from . import analytical
from . import wish_simulator
from . import models
from . import forms
from genshinwishoracle.project_primos import project_future_primos, project_primos_chart
from users.models import Profile

class Address():
    def __init__(self, url:str, name:str) -> None:
        self.url = url
        self.name = name

class IndexView(generic.ListView):
    context_object_name = 'urls'
    template_name = 'genshinwishoracle/index.html'
    url_names = [['statistics', {"banner_type": "character", "statistics_type": "calcprobability" }, "Wishing Statistics"], ['character_banners',{}, "Character Banners"], ['weapon_banners',{}, "Weapon Banners"], ['project_primos',{}, "Project Future Primogems"],['wish_simulator',{}, "Wishing Simulator"], ['users:users-home',{}, "User Login and Settings"]]

    def get_context_data(self, **kwargs):
        context = {}
        context[self.context_object_name] = self.get_queryset()
        return context

    def get_queryset(self):
        urls = []
        for item in self.url_names:
            urls.append(Address(str(reverse(item[0], kwargs = item[1])), item[2]))
        return urls

# BANNER LIST
# USED AS ABSTRACT CLASS
class BannerView(generic.ListView):
    banner_type = ""
    template_name = 'analyze/banners_list.html'
    context_object_name = 'banners'
    back_url = reverse_lazy('main-home')
    create_url = reverse_lazy(banner_type.lower()+'_banner_create')
    labels = []
    # TODO see if I want this
    # paginate_by = 5

    def get_context_data(self, **kwargs):
        context = {}
        banners =self.get_queryset(self.request)
        context[self.context_object_name] = banners
        context['labels'] = self.labels
        context['back_url'] = self.back_url
        context['create_url'] = self.create_url
        context['url_front'] = "/"+self.banner_type.lower()+"-banners"
        context['banner_type'] = self.banner_type
        return context

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to=reverse_lazy('main-home'))
        context = self.get_context_data()
        return render(request, self.template_name, context=context)

    def get_queryset(self,request):
        curr_user_prof = Profile.objects.filter(user_id = request.user.id)[0]
        banners = curr_user_prof.banners.filter(banner_type=self.model.get_banner_type_string())
        banners = [banner.get_specified_banner_equivalent() for banner in banners]
        return banners
    
class CharacterBannerView(BannerView):
    model = models.CharacterBanner
    banner_type = "Character"
    create_url = reverse_lazy(banner_type.lower()+'_banner_create')
    labels = ["Name", "Enddate", "5⭐ Rateup", "4⭐ Rateup 1", "4⭐ Rateup 2", "4⭐ Rateup 3", "Edit", "Delete"]
    # TODO see if I want this
    # paginate_by = 5

class WeaponBannerView(BannerView):
    model = models.WeaponBanner
    banner_type = "Weapon"
    create_url = reverse_lazy(banner_type.lower()+'_banner_create')
    labels = ["Name", "Enddate", "5⭐ Rateup 1","5⭐ Rateup 2", "4⭐ Rateup 1", "4⭐ Rateup 2", "4⭐ Rateup 3", "4⭐ Rateup 4", "4⭐ Rateup 5", "Edit", "Delete"]

# DELETE VIEW
# USED AS ABSTRACT CLASS
class BannerDeleteView(generic.DeleteView):
    banner_type = ""
    template_name = 'analyze/banner_delete.html'
    success_url = reverse_lazy(banner_type.lower()+'_banners')
    labels = []

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['success_url'] = self.success_url
        context['banner_type'] = self.banner_type
        context['banner'] = context['object']
        context['labels'] = self.labels
        return context

class CharacterBannerDeleteView(BannerDeleteView):
    model = models.CharacterBanner
    banner_type = "Character"
    success_url = reverse_lazy(banner_type.lower()+'_banners')
    labels = ["Name", "Enddate", "5⭐ Rateup", "4⭐ Rateup 1", "4⭐ Rateup 2", "4⭐ Rateup 3"] 

class WeaponBannerDeleteView(BannerDeleteView):
    model = models.WeaponBanner
    banner_type = "Weapon"
    success_url = reverse_lazy(banner_type.lower()+'_banners')
    labels = ["Name", "Enddate", "5⭐ Rateup 1","5⭐ Rateup 2", "4⭐ Rateup 1", "4⭐ Rateup 2", "4⭐ Rateup 3", "4⭐ Rateup 4", "4⭐ Rateup 5"]

# UPDATE VIEW
# USED AS ABSTRACT CLASS
class BannerUpdateView(generic.UpdateView):
    template_name = 'analyze/banner_update.html'
    banner_type = ""
    context_object_name = 'banner'
    success_url = reverse_lazy('character_banners')
    form_class = forms.forms.BaseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_url'] = self.success_url
        context['banner_type'] = self.banner_type
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        kwargs["updating"] = True
        return kwargs

    def post(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to=reverse_lazy('main-home'))
        context ={}
        banner_before = self.model.objects.filter(id=kwargs['pk'])
        kwargs = self.get_form_kwargs()
        kwargs["data"] = self.request.POST
        form  = self.form_class(**kwargs)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            rateups = cleaned_data.pop('rateups')
            banner_before.update(**cleaned_data)
            banner_before[0].rateups.set(rateups)
            return redirect(to=self.success_url)
        else:
            context['form'] = form
            return render(request, self.template_name, context=context)
    
class CharacterBannerUpdateView(BannerUpdateView):
    model = models.CharacterBanner
    banner_type = "Character"
    success_url = reverse_lazy(banner_type.lower()+'_banners')
    form_class = forms.CreateCharacterBannerForm
class WeaponBannerUpdateView(BannerUpdateView):
    model = models.WeaponBanner
    banner_type = "Weapon"
    success_url = reverse_lazy(banner_type.lower()+'_banners')
    form_class = forms.CreateWeaponBannerForm

# CREATE VIEW

class BannerCreateView(generic.CreateView):
    model = models.CharacterBanner
    form_class = forms.CreateCharacterBannerForm
    template_name = 'analyze/banner_create.html'
    success_url = reverse_lazy('character_banners')
    banner_type = "Character"
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        kwargs["updating"] = False
        return kwargs

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to=reverse_lazy('main-home'))
        context = {}
        kwargs = {}
        kwargs.update({"user_id": request.user.id})
        form = self.form_class(**kwargs)
        context['form'] = form
        context['banner_type'] = self.banner_type
        context['success_url' ] = self.success_url
        return render(request, self.template_name, context=context)

    def post(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to=reverse_lazy('main-home'))
        context ={}
        kwargs = self.get_form_kwargs()
        kwargs["data"] = self.request.POST
        form  = self.form_class(**kwargs)
        if form.is_valid():
            character_banner = form.save()
            profile = Profile.objects.filter(user_id= request.user.id).first()
            profile.banners.add(character_banner)
            return redirect(to=self.success_url)
        else:
            context['form'] = form
            return render(request, self.template_name, context=context)

class CharacterBannerCreateView(generic.CreateView):
    model = models.CharacterBanner
    form_class = forms.CreateCharacterBannerForm
    template_name = 'analyze/banner_create.html'
    success_url = reverse_lazy('character_banners')
    banner_type = "Character"
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        kwargs["updating"] = False
        return kwargs

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to=reverse_lazy('main-home'))
        context = {}
        kwargs = {}
        kwargs.update({"user_id": request.user.id})
        form = self.form_class(**kwargs)
        context['form'] = form
        context['banner_type'] = self.banner_type
        context['success_url' ] = self.success_url
        return render(request, self.template_name, context=context)

    def post(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to=reverse_lazy('main-home'))
        context ={}
        kwargs = self.get_form_kwargs()
        kwargs["data"] = self.request.POST
        form  = self.form_class(**kwargs)
        if form.is_valid():
            character_banner = form.save()
            profile = Profile.objects.filter(user_id= request.user.id).first()
            profile.banners.add(character_banner)
            return redirect(to=self.success_url)
        else:
            context['form'] = form
            return render(request, self.template_name, context=context)


class WeaponBannerCreateView(generic.CreateView):
    model = models.WeaponBanner
    form_class = forms.CreateWeaponBannerForm
    banner_type = "Weapon"
    template_name = 'analyze/banner_create.html'
    success_url = reverse_lazy('weapon_banners')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        kwargs["updating"] = False
        return kwargs

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to=reverse_lazy('main-home'))
        context = {}
        kwargs = self.get_form_kwargs()
        form = self.form_class(**kwargs)
        context['form'] = form
        context['banner_type'] = self.banner_type
        context['success_url' ] = self.success_url
        return render(request, self.template_name, context=context)

    def post(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to=reverse_lazy('main-home'))
        context ={}
        kwargs = self.get_form_kwargs()
        kwargs['data'] = self.request.POST
        form  = self.form_class(**kwargs)
        if form.is_valid():
            weapon_banner = form.save()
            print(request.user.id)
            profile = Profile.objects.get(user_id= request.user.id)
            profile.banners.add(weapon_banner)
            return redirect(to=self.success_url)
        else:
            context['form'] = form
            return render(request, self.template_name, context=context)

class StatisticsAnalyzeOmniView(generic.View):
    template_name = 'analyze/analyze_omni.html'
    result_template = 'analyze/analyze_results.html'
    valid_banner_types = ['character', 'weapon']
    valid_statistics_types = ['calcprobability', 'calcnumwishes']
    default_url = "/{}/{}/".format(valid_banner_types[0], valid_statistics_types[0])

    def get(self, request,banner_type, statistics_type, *args, **kwargs):
        if banner_type not in self.valid_banner_types or statistics_type not in self.valid_statistics_types:
            return redirect(to=self.default_url)
        context = {"banner_type":banner_type,"statistics_type": statistics_type }
        first_form = self.get_first_form(banner_type=banner_type,statistics_type=statistics_type)
        request.session['import_data'] = False
        context["first_form"] = first_form
        second_form_names =  self.get_second_form_names(banner_type=banner_type,statistics_type=statistics_type,first_form=first_form)
        context["second_form_names"] = second_form_names

        return render(request, self.template_name, context=context)

    def get_first_form(self, banner_type, statistics_type):
        request = self.request
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
    
    def get_second_form_names(self, banner_type, statistics_type,first_form):
        if statistics_type == "calcprobability" and banner_type == "character":
            form = forms.AnalyzeStatisticsCharacterToNumWishesForm()
        elif statistics_type == "calcprobability" and banner_type == "weapon":
            form = forms.AnalyzeStatisticsWeaponToNumWishesForm()
        elif statistics_type == "calcnumwishes" and banner_type == "character":
            form = forms.AnalyzeStatisticsCharacterToProbabilityForm()
        elif statistics_type == "calcnumwishes" and banner_type == "weapon":
            form = forms.AnalyzeStatisticsWeaponToProbabilityForm()
        # technically could just remove pity/guaranteed/fate_points
        names = []
        for field in form.fields:
            if field not in first_form.Meta.fields:
                names.append(form[field].label)
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
                return redirect(to=reverse('statistics', kwargs={"banner_type":banner_type, "statistics_type":statistics_type}))
        elif request.POST.get("reset_values"):
            request.session.pop('wishes')
            request.session['import_data'] = False
            context = {"banner_type":banner_type,"statistics_type": statistics_type }
            first_form = self.get_first_form(banner_type=banner_type,statistics_type=statistics_type)
            context["first_form"] = first_form
            second_form_names =  self.get_second_form_names(banner_type=banner_type,statistics_type=statistics_type,first_form=first_form)
            context["second_form_names"] = second_form_names
            return render(request, self.template_name, context=context)
        if request.POST.get("reset"):
            if 'wishes' in request.session:
                request.session.pop('wishes')
        request.session['import_data'] = False
        # add request post to the correct type given by function
        form = self.get_first_form(banner_type,statistics_type)
        if form.is_valid():
            cleaned = form.cleaned_data
            place_values = 3 
            if banner_type == "character" and statistics_type == "calcprobability":
                analyze_obj = analytical.AnalyticalCharacter()
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
                context['chart'] = analytical.bar_graph_for_statistics(solution,banner_type, statistics_type, cleaned['numwishes'],cleaned['pity'],cleaned['guaranteed'],0)
            elif banner_type == "weapon" and statistics_type == "calcprobability":
                analyze_obj = analytical.AnalyticalWeapon()
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
                context['chart'] = analytical.bar_graph_for_statistics(solution,banner_type, statistics_type, cleaned['numwishes'],cleaned['pity'],cleaned['guaranteed'],cleaned['fate_points'])
            elif banner_type == "character" and statistics_type == "calcnumwishes":
                analyze_obj = analytical.AnalyticalCharacter()
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
                analyze_obj = analytical.AnalyticalWeapon()
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
        first_form = self.get_first_form(banner_type=banner_type,statistics_type=statistics_type)
        context["first_form"] = first_form
        second_form_names =  self.get_second_form_names(banner_type=banner_type,statistics_type=statistics_type,first_form=first_form)
        context["second_form_names"] = second_form_names
        return render(request, self.template_name, context)

    def button_name_post_to_redirect(self, request, banner_type, statistics_type):
        if request.POST.get("select_weapon_banner"):
            return redirect(to='/statistics/weapon/{}/'.format(statistics_type))
        elif request.POST.get("select_character_banner"):
            return redirect(to='/statistics/character/{}/'.format(statistics_type))
        if request.POST.get("select_calcnumwishes"):
            return redirect(to='/statistics/{}/calcnumwishes/'.format(banner_type))
        elif request.POST.get("select_calcprobability"):
            return redirect(to='/statistics/{}/calcprobability/'.format(banner_type))
        else:
            return None
class StatisticsResultView(generic.View):
    template_name = 'analyze/analyze_results.html'
    success_url = reverse_lazy('main-home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data
        
class ProjectPrimosView(generic.FormView):
    template_name = 'analyze/project_primos.html'
    result_template = 'analyze/project_primos_result.html'
    success_url = reverse_lazy('project_primos_results')
    form_class = forms.ProjectPrimosForm

    def get(self, request,*args, **kwargs):
        context = {}
        kwargs = {}
        if request.user.is_authenticated:
            curr_user_prof = Profile.objects.filter(user_id = request.user.id)[0]
            kwargs.update({'user_id': request.user.id})
        # using sessions here since I prefer a flag on the user rather than making the url look worse personally
        if 'import_data' in request.session and request.session['import_data'] == True:
            request.session['import_data'] = False
            init = {'numprimos': curr_user_prof.numprimos, 'numgenesis': curr_user_prof.numgenesis, 'numfates': curr_user_prof.numfates, 'numstarglitter': curr_user_prof.numstarglitter}
            context['form'] = self.form_class(initial=init, **kwargs)
        else:
            context['form'] = self.form_class(**kwargs)

        return render(request, self.template_name, context=context)

    def post(self, request,*args, **kwargs):
        context ={}
        kwargs = {}
        if request.user.is_authenticated:
            curr_user_prof = Profile.objects.filter(user_id = request.user.id)[0]
            kwargs.update({'user_id': request.user.id})
        if request.POST.get("import_user_data"):
            if request.user.is_authenticated:
                request.session["import_data"] = True
                return redirect(to=reverse_lazy('project_primos'))
        elif request.POST.get("reset_values"):
            form  = forms.ProjectPrimosForm(**kwargs)
            context['form'] = form
            return render(request, 'analyze/project_primos.html', context=context)
        elif request.POST.get("analyze_with_future_primogems"):
            request.session["wishes"] = request.POST.get("analyze_with_future_primogems")
            banner_type = "character"
            statistics_type = "calcprobability"
            return redirect(to=reverse('statistics', kwargs={"banner_type":banner_type, "statistics_type":statistics_type}))
        form  = forms.ProjectPrimosForm(request.POST,**kwargs)
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
            current_date = timezone.now().date()
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
            chart = project_primos_chart(current_primos, 0,0,0,days_until_enddate,cleaned['welkin_moon'],cleaned['battlepass'], cleaned['average_abyss_stars'])
            context['chart'] = chart
            return render(request, self.result_template, context=context)
        elif not form.date_is_decidable():
            form.add_error('end_date_manual_select', "Please add a manual banner end date or select a banner for its end date.")
            context['form'] = form
            return render(request, self.template_name, context=context)
        else:
            context['form'] = form
            return render(request, self.template_name, context=context)
class WishSimulatorView(generic.View):
    template_name = 'analyze/wish_simulator.html'
    success_url = reverse_lazy('main-home')
    form_class = forms.WishSimulatorForm
    
    def get_form_kwargs(self):
        kwargs = {}
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def get(self, request,*args, **kwargs):
        context = {}
        kwargs = self.get_form_kwargs()
        context['form'] = self.form_class(**kwargs)
        return render(request, self.template_name,context=context)
    def post(self, request,*args, **kwargs):
        kwargs = self.get_form_kwargs()
        kwargs['data'] = request.POST
        form = self.form_class(**kwargs)
        if form.is_valid():
            number_of_pulls = request.POST['number_of_pulls']
            banner_id = request.POST['banner']
            return redirect(to=reverse('wish_simulator_result', kwargs={"number_of_pulls":number_of_pulls,'banner_id': banner_id}))
        else:
            context = {}
            context['form'] = self.form_class
            return render(request, self.template_name,context=context)

class WishSimulatorResultsView(generic.ListView):
    template_name = 'analyze/wish_simulator_result.html'
    success_url = reverse_lazy('main-home')

    def get(self, request,banner_id, number_of_pulls,*args, **kwargs):
        context ={}
        context['number_of_pulls'] = number_of_pulls
        pulls = self.wish_simulator(number_of_pulls, banner_id)
        ten_pulls = []
        i = 0
        for i in range(0,math.floor(len(pulls) / 10)):
            ten_pull = []
            for j in range(0,10):
                ten_pull.append(pulls[i*10+j])
            ten_pulls.append(ten_pull)
        ten_pull = []
        for k in range(0,len(pulls) % 10):
            k
            ten_pull.append(pulls[(i)*10+k])
        if ten_pull != []:
            ten_pulls.append(ten_pull)
        context['ten_pulls'] = ten_pulls
        return render(request, self.template_name, context=context)

    def get_queryset(self):
        pass
    
    def get_context_data(self,**kwargs):
        context = super(generic.ListView, self).get_context_data(**kwargs)
        return context

    def wish_simulator(self, number_of_pulls, banner):
        five_star_pity = 0
        five_star_guaranteed = False
        four_star_pity = 0 
        four_star_guaranteed = False
        fate_points = 0
        banner = models.Banner.objects.filter(id=banner).first()
        rateups= banner.get_specified_banner_equivalent().rateups.all()
        simulator = wish_simulator.WishSim(banner,rateups.filter(rarity=5).first())
        pulls = simulator.roll(number_of_pulls,five_star_pity,five_star_guaranteed,four_star_pity,four_star_guaranteed, fate_points)
        return pulls

    

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