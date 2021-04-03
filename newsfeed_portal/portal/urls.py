from django.urls import path
from .views import *

app_name = 'portal'

urlpatterns = [
    path('aljazeera/', AlJazeera, name = 'AlJazeera'),
    path('bbc/', BBC, name = 'BBC'),

    path('home/', HomeView.as_view(), name='home'),
]
