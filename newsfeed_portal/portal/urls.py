from django.urls import path
from .views import *

app_name = "portal"

urlpatterns = [
    path("aljazeera/", AlJazeera, name="AlJazeera"),
    path("bbc/", BBC, name="BBC"),
    path("user-home/", UserHomeView.as_view(), name="user_home"),
    path(
        "user-country-based-news/",
        UserCountryBasedNewsView.as_view(),
        name="user_country_based_news",
    ),
    path(
        "user-source-based-news/",
        UserSourceBasedNewsView.as_view(),
        name="user_source_based_news",
    ),
    path(
        "user-keyword-based-news/",
        UserKeywordBasedNewsView.as_view(),
        name="user_keyword_based_news",
    ),
    path("user-profile-settings/", user_profile_settings, name="user_profile_settings"),
    path(
        "user-news-recommend-settings/",
        user_news_recommend_settings,
        name="user_news_recommend_settings",
    ),
    path(
        "user-news-recommend-settings/category-manager/",
        user_news_recommend_settings_category_manager,
        name="user_news_recommend_settings_category_manager",
    ),
]
