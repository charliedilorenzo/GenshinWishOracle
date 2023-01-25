from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'analyze'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('characterbanner/', views.CharacterBannerView.as_view(), name='character_banner'),
    path('characterbanner/create', views.CharacterBannerCreateView.as_view(), name='character_banner_create'),
    path('weaponbanner/', views.WeaponBannerView.as_view(), name='weapon_banner'),
    path('weaponbanner/create', views.WeaponBannerCreateView.as_view(), name='weapon_banner_create'),
    path('statistics/character/', views.StatisticsAnalyzeCharacterView.as_view(), name='analyze_statistics_character'),
    path('statistics/weapon/', views.StatisticsAnalyzeWeaponView.as_view(), name='analyze_statistics_weapon'),
    path('statistics/results',views.StatisticsResultView.as_view(), name='analyze_results'),
    path('projectprimos',views.ProjectPrimosView.as_view(), name='project_primos'),
    path('projectprimos/results', views.project_primos_in_progress, name='project_primos_in_progress'),
    path('projectprimos/results',views.ProjectPrimosResultsView.as_view(), name='project_primos_results'),
    path('probability-to-wishes-required',views.ProbabilityToWishesView.as_view(), name='probability_to_wishes'),
    # TODO add data, edit data, delete
    path('user-data',views.UserDataView.as_view(), name='user_data'),
    path('wishsimulator',views.WishSimulatorView.as_view(), name='wish_simulator'),
]
urlpatterns += staticfiles_urlpatterns()