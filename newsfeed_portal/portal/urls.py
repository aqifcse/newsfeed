from django.urls import path
from .views import *

app_name = "portal"

urlpatterns = [
    path("user-home/", user_home, name="user_home"),
    path("user-profile-settings/", user_profile_settings, name="user_profile_settings"),
    path(
        "user-news-recommend-settings/",
        user_news_recommend_settings,
        name="user_news_recommend_settings",
    ),
]
