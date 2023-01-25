
from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from . import forms

app_name = 'users'
urlpatterns = [
    path('', views.home, name='users-home'),
    path('register/', views.RegisterView.as_view(), name='users-register'), 
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=forms.LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='users-profile'),
]