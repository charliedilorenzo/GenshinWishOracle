from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'analyze'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('characterbanner/', views.CharacterBannerView.as_view(), name='characterbanner'),
    path('characterbanner/create', views.CharacterBannerCreateView.as_view(), name='characterbannercreate'),
    path('weaponbanner/', views.WeaponBannerView.as_view(), name='weaponbanner'),
    path('weaponbanner/create', views.WeaponBannerCreateView.as_view(), name='weaponbannercreate'),
    path('statistics/character/', views.StatisticsAnalyzeCharacterView.as_view(), name='analyze_statistics_character'),
    path('statistics/weapon/', views.switch_banner_type_character, name='switch_banner_type_character'),
    path('statistics/weapon/', views.StatisticsAnalyzeWeaponView.as_view(), name='analyze_statistics_weapon'),
    path('statistics/character/', views.switch_banner_type_weapon, name='switch_banner_type_weapon'),
    path('statistics/results', views.analysis_in_progress, name='analysis_in_progress'),
    path('statistics/results',views.StatisticsResultView.as_view(), name='analyze_results'),
]

urlpatterns += staticfiles_urlpatterns()