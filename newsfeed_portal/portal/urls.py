from django.urls import path
from .views import *

app_name = 'portal'

urlpatterns = [
    path('aljazeera/', AlJazeera, name = 'AlJazeera'),
    path('bbc/', BBC, name = 'BBC'),
    
    path('user-home/', UserHomeView.as_view(), name='user_home'),
    path('user-country-based-news/', UserCountryBasedNewsView.as_view(), name='user_country_based_news'),
    path('user-source-based-news/', UserSourceBasedNewsView.as_view(), name='user_source_based_news'),
    path('user-keyword-based-news/', UserKeywordBasedNewsView.as_view(), name='user_keyword_based_news'),

    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    #path('settings/', SettingsView.as_view(), name='settings'),
]
