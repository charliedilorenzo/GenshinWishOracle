
from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from . import forms

app_name = 'users'
urlpatterns = [
    path('', views.home, name='users-home'),
    path('register/', views.RegisterView.as_view(), name='users-register'), 
    path('profile/', views.profile, name='users-profile'),
]