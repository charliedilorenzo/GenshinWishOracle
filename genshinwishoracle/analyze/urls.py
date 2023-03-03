from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'analyze'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
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
]
urlpatterns += staticfiles_urlpatterns()