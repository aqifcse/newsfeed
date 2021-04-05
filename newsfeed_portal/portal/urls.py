from django.urls import path
from .views import *

app_name = 'portal'

urlpatterns = [
    path('aljazeera/', AlJazeera, name = 'AlJazeera'),
    path('bbc/', BBC, name = 'BBC'),
    path('user-home/', UserHomeView.as_view(), name='user_home'),
    path('profile/', profile, name='profile'),
]
