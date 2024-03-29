"""genshinwishoracle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from users.views import ResetPasswordView, ChangePasswordView,CustomLoginView, password_reset_request
from . import views
from django.contrib.auth import views as auth_views
from users.forms import LoginForm
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.IndexView.as_view(), name='main-home'),
    path('character-banners/', views.CharacterBannerView.as_view(), name='character_banners'),
    path('character-banners/create', views.CharacterBannerCreateView.as_view(), name='character_banner_create'),
    path('character-banners/<pk>/delete', views.CharacterBannerDeleteView.as_view(), name='character_banner_delete'),
    path('character-banners/<pk>', views.CharacterBannerUpdateView.as_view(), name='character_banner_update'),
    path('weapon-banners/', views.WeaponBannerView.as_view(), name='weapon_banners'),
    path('weapon-banners/create', views.WeaponBannerCreateView.as_view(), name='weapon_banner_create'),
    path('weapon-banners/<pk>/delete', views.WeaponBannerDeleteView.as_view(), name='weapon_banner_delete'),
    path('weapon-banners/<pk>', views.WeaponBannerUpdateView.as_view(), name='weapon_banner_update'),
    path('statistics/<str:banner_type>/<str:statistics_type>/', views.StatisticsAnalyzeOmniView.as_view(), name="statistics"),
    path('statistics/results',views.StatisticsResultView.as_view(), name='analyze_results'),
    path('project-primos/',views.ProjectPrimosView.as_view(), name='project_primos'),
    path('wish-simulator/',views.WishSimulatorView.as_view(), name='wish_simulator'),
    path('wish-simulator/<int:banner_id>/<int:number_of_pulls>/',views.WishSimulatorResultsView.as_view(), name='wish_simulator_result'),
    path('demo',TemplateView.as_view(template_name="bootstrap_base.html"),name='demo'),
    path('popovers',TemplateView.as_view(template_name="bootstrap_popovers.html"), name="popovers"),
    path('admin/', admin.site.urls, name='admin'),
    path('analyze/', include('analyze.urls'), name='analyze_index'),
    path('users/', include('users.urls'), name='users-home'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('favicon.ico',RedirectView.as_view(url='/static/base/icons/favicon.ico')),
    path('jsi18n', JavaScriptCatalog.as_view(), name='jsi18n'),
    path('oauth/', include('social_django.urls',namespace='social'), name='social'),
    path('credits/', views.CreditsView.as_view(), name="credits"),
    path('about/', views.AboutView.as_view(), name="about"),
]
