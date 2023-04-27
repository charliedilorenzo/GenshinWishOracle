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
from . import helpers
from .helpers import PersonalizedLoginRequiredMixin
from .project_primos import project_future_primos, project_primos_chart
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
class BannerView(PersonalizedLoginRequiredMixin, generic.ListView):
    banner_type = ""
    template_name = 'analyze/banners_list.html'
    context_object_name = 'banners'
    back_url = reverse_lazy('main-home')
    create_url = reverse_lazy(banner_type.lower()+'_banner_create')
    labels = []
    special_template = 'analyze/banners_list_empty.html'
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
        context = self.get_context_data()
        profile = Profile.objects.filter(user_id = request.user.pk).first()
        if not profile.user_has_any_banner_type(self.banner_type):
            return render(request, self.special_template, context=context)
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
class BannerDeleteView(PersonalizedLoginRequiredMixin,generic.DeleteView):
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

    def get(self, request, *args, **kwargs):
        parent_get = super().get(request, *args, **kwargs)
        context = self.get_context_data()
        banner = context['banner']
        profile = Profile.objects.filter(user_id=request.user).first()
        user_banner_ids = profile.banners.values_list('pk',flat=True)
        # REDIRECT WRONG USER
        if banner.id not in user_banner_ids:
            return redirect(to=self.success_url)

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        parent_post = super().post(request, *args, **kwargs)
        profile = Profile.objects.filter(user_id=request.user).first()
        user_banner_ids = profile.banners.values_list('pk',flat=True)
        # REDIRECT WRONG USER
        if kwargs['pk'] not in user_banner_ids:
            return redirect(to=self.success_url)
        return parent_post

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
class BannerUpdateView(PersonalizedLoginRequiredMixin,generic.UpdateView):
    template_name = 'analyze/banner_update.html'
    banner_type = ""
    context_object_name = 'banner'
    success_url = reverse_lazy(banner_type.lower()+'_banners')
    form_class = forms.forms.BaseForm

    def get(self, request, *args, **kwargs):
        parent_get = super().get(request, *args, **kwargs)
        context = self.get_context_data()
        banner = context['banner']
        profile = Profile.objects.filter(user_id=request.user).first()
        user_banner_ids = profile.banners.values_list('pk',flat=True)
        # REDIRECT WRONG USER
        if banner.id not in user_banner_ids:
            return redirect(to=self.success_url)

        return render(request, self.template_name, context=context)

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
        
        profile = Profile.objects.filter(user_id=request.user).first()
        user_banner_ids = profile.banners.values_list('pk',flat=True)
        # REDIRECT WRONG USER
        if kwargs['pk']  not in user_banner_ids:
            return redirect(to=self.success_url)

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

class BannerCreateView(PersonalizedLoginRequiredMixin,generic.CreateView):
    model = models.CharacterBanner
    banner_type = ""
    form_class = forms.forms.BaseForm
    template_name = 'analyze/banner_create.html'
    success_url = reverse_lazy(banner_type.lower()+'_banners')
    

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

class CharacterBannerCreateView(BannerCreateView):
    model = models.CharacterBanner
    form_class = forms.CreateCharacterBannerForm
    banner_type = "Character"
    success_url = reverse_lazy(banner_type.lower()+'_banners')
class WeaponBannerCreateView(BannerCreateView):
    model = models.WeaponBanner
    form_class = forms.CreateWeaponBannerForm
    banner_type = "Weapon"
    success_url = reverse_lazy(banner_type.lower()+'_banners')

# ANALYZE

class StatisticsAnalyzeOmniView(generic.View):
    template_name = 'analyze/analyze_omni.html'
    result_template = 'analyze/analyze_results.html'
    valid_banner_types = ['character', 'weapon']
    valid_statistics_types = ['calcprobability', 'calcnumwishes']
    default_url = "/{}/{}/".format(valid_banner_types[0], valid_statistics_types[0])
    forms_dictionary =  {"calcprobability": 
                      {"character": forms.AnalyzeStatisticsCharacterToProbabilityForm,"weapon":forms.AnalyzeStatisticsWeaponToProbabilityForm },
                      "calcnumwishes": 
                      {"character": forms.AnalyzeStatisticsCharacterToNumWishesForm,"weapon":forms.AnalyzeStatisticsWeaponToNumWishesForm }
                      }

    def get_context_data(self, banner_type,statistics_type, **kwargs):
        context = {"banner_type":banner_type,"statistics_type": statistics_type }
        first_form = self.get_first_form(banner_type=banner_type,statistics_type=statistics_type)
        self.request.session['import_data'] = False
        context["first_form"] = first_form
        second_form_names =  self.get_second_form_names(banner_type=banner_type,statistics_type=statistics_type,first_form=first_form)
        context["second_form_names"] = second_form_names
        return context

    def get(self, request,banner_type, statistics_type, *args, **kwargs):
        if banner_type not in self.valid_banner_types or statistics_type not in self.valid_statistics_types:
            return redirect(to=self.default_url)
        context = self.get_context_data(banner_type,statistics_type)
        return render(request, self.template_name, context=context)

    def get_first_form(self, banner_type, statistics_type):
        request = self.request
        init = {}
        form = self.forms_dictionary[statistics_type][banner_type]
        if request.POST:
            request.session['wishes'] = None
            form = form(request.POST)
            return form
        elif 'import_data' in request.session and request.session['import_data'] == True:
            if request.user.is_authenticated:
                curr_user_prof = Profile.objects.filter(user_id = request.user.id)[0]
                init = helpers.import_user_data(curr_user_prof, form)
        # not very elegant but alternatives also seems to suck
        elif request.session.setdefault('wishes', None) is not None:
            init.update({'numwishes': request.session['wishes']})
        form = form(initial=init)
        return form

    def get_second_form_names(self, banner_type, statistics_type,first_form):
        statistics_type = self.opposite(statistics_type)
        form = self.forms_dictionary[statistics_type][banner_type]()
        # technically could just remove pity/guaranteed/fate_points
        names = []
        for field in form.fields:
            if field not in first_form.Meta.fields:
                names.append(form[field].label)
        return names

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
            context = self.get_context_data(banner_type,statistics_type)
            return render(request, self.template_name, context=context)
        request.session['import_data'] = False
        # add request post to the correct type given by function
        form = self.get_first_form(banner_type,statistics_type)
        if form.is_valid():
            cleaned = form.cleaned_data
            context = cleaned
            if banner_type == "character":
                analyze_obj = analytical.AnalyzeCharacter()
            elif banner_type == "weapon":
                analyze_obj = analytical.AnalyzeWeapon()

            if statistics_type == "calcprobability":
                statistics = analyze_obj.get_statistic(cleaned['numwishes'],cleaned['pity'],cleaned['guaranteed'],cleaned.setdefault('fate_points', 0),0,True)
                context.update({
                    'banner_type' : banner_type.capitalize(),
                    'statistics_type': statistics_type,
                    "statistics": statistics
                })
                context['chart'] = analytical.bar_graph_for_statistics(statistics.get_formated_dictionary() , **context)
            elif statistics_type == "calcnumwishes":
                numwishes = analyze_obj.probability_on_copies_to_num_wishes(cleaned['minimum_probability'], cleaned['numcopies'],cleaned['pity'], cleaned['guaranteed'])
                context.update({
                    'banner_type' : banner_type.capitalize(),
                    'statistics_type': statistics_type,
                    'numwishes': numwishes
                })
                chart = ""
            return render(request, self.result_template, context)
        request.session.pop('wishes')
        request.session['import_data'] = False
        context = self.get_context_data(banner_type, statistics_type)
        return render(request, self.template_name, context)

    def button_name_post_to_redirect(self, request, banner_type, statistics_type):
        if request.POST.get("banner_type"):
            return redirect(to='/statistics/{}/{}/'.format(self.opposite(banner_type),statistics_type))
        elif request.POST.get("statistics_type"):
            return redirect(to='/statistics/{}/{}/'.format(banner_type,self.opposite(statistics_type)))
        
    def opposite(self,string):
        opposite_dictionary = {self.valid_banner_types[0]: self.valid_banner_types[1], self.valid_banner_types[1]: 
                               self.valid_banner_types[0], self.valid_statistics_types[0]: self.valid_statistics_types[1],
                               self.valid_statistics_types[1]:self.valid_statistics_types[0]}
        return opposite_dictionary[string]
class StatisticsResultView(generic.View):
    template_name = 'analyze/analyze_results.html'
    success_url = reverse_lazy('main-home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return data

# PROJECT PRIMOS

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
            init = {'numprimos': curr_user_prof.numprimos, 'numgenesis': curr_user_prof.numgenesis, 'numfates': curr_user_prof.numfates, 'numstarglitter': curr_user_prof.numstarglitter, "battlepass": curr_user_prof.battlepass_user, "welkin_moon": curr_user_prof.welkin_user}
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
            context['form'] = forms.ProjectPrimosForm(**kwargs)
            return render(request, 'analyze/project_primos.html', context=context)
        elif request.POST.get("analyze_with_future_primogems"):
            request.session["wishes"] = request.POST.get("analyze_with_future_primogems")
            # TODO possibly switch to be two buttons with one for character and one for weapon
            return redirect(to=reverse('statistics', kwargs={"banner_type":"character", "statistics_type":"calcprobability"}))
        form  = forms.ProjectPrimosForm(request.POST,**kwargs)
        if form.is_valid():
            cleaned = form.cleaned_data
            future_date = form.decide_date()
            now = datetime.date.today()
            days_until_enddate = (future_date-now).days
            # TODO test if we need this
            if days_until_enddate < 0:
                # non-sensical end date
                return render(request, self.template_name)
            current_date = timezone.now().date()
            current_primos = cleaned['numprimos']+cleaned['numgenesis']+160*math.floor(cleaned['numstarglitter']/5)+ 160*cleaned['numfates']

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
        context['form'] = form
        return render(request, self.template_name, context=context)
        
# WISH SIMULATOR
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