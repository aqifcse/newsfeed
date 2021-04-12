from django.urls import path
from .views import *

app_name = "portal"

urlpatterns = [
    path("user-home/", user_home, name="user_home"),
    path("user-profile-settings/", user_profile_settings, name="user_profile_settings"),
    path(
        "create-readlist/",
        user_create_readlist,
        name="user_create_readlist",
    ),
    path(
        "manage-readlist/",
        ManageReadListsView.as_view(),
        name="user_manage_readlists",
    ),
    path(
        "top-headlines/",
        user_top_headlines,
        name="user_top_headlines",
    ),
    path(
        "full-stories/",
        user_full_stories,
        name="user_full_stories",
    ),
]
