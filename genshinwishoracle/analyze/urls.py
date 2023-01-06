from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'analyze'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('characterbanner/', views.CharacterBannerView.as_view(), name='characterbanner'),
    path('characterbanner/create', views.CharacterBannerCreateView.as_view(), name='characterbannercreate'),
    path('weaponbanner/', views.WeaponBannerView.as_view(), name='weaponbanner'),
    path('weaponbanner/create', views.WeaponBannerView.as_view(), name='weaponbannercreate'),
    path('statistics/', views.StatisticsAnalyzeView.as_view(), name='analyzestatistics'),
]