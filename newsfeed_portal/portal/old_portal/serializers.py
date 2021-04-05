from rest_framework.serializers import ModelSerializer

from .models import User, App, AppAuthor
from rest_framework import serializers


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'is_active'
        ]


class AppCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = App
        fields = [
            'is_active'        
        ]

class DownloadCountSerializer(ModelSerializer):
    
    class Meta:
        model = App
        fields = ('downloads',)

