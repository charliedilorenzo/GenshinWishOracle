from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'analyze'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('character-banner/', views.CharacterBannerView.as_view(), name='character_banner'),
    path('character-banner/create', views.CharacterBannerCreateView.as_view(), name='character_banner_create'),
    path('weapon-banner/', views.WeaponBannerView.as_view(), name='weapon_banner'),
    path('weapon-banner/create', views.WeaponBannerCreateView.as_view(), name='weapon_banner_create'),
    path('statistics/<str:banner_type>/<str:statistics_type>/', views.StatisticsAnalyzeOmniView.as_view(), name="statistics"),
    path('statistics/results',views.StatisticsResultView.as_view(), name='analyze_results'),
    path('project-primos/',views.ProjectPrimosView.as_view(), name='project_primos'),
    path('wish-simulator/',views.WishSimulatorView.as_view(), name='wish_simulator'),
    path('wish-simulator/<int:banner_id>/<int:number_of_pulls>/',views.WishSimulatorResultsView.as_view(), name='wish_simulator_result'),
]
urlpatterns += staticfiles_urlpatterns()