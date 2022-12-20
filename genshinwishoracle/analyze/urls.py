from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('characterbanner/', views.AnalyzeCharacterBannerView.as_view(), name='index'),
    # path('weaponbanner/', views.AnalyzeWeaponBannerView.as_view(), name='index'),
]