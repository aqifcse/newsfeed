from django.urls import path
from .views import AlJazeera, BBC

urlpatterns = [
path('al-jazeera/', AlJazeera, name = 'AlJazeera'),
path('bbc/', BBC, name = 'BBC')

]
