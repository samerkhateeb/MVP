from rest_framework import serializers
from auth_user.models import TempFiles, UserProfile
from django.conf import settings

class TempFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempFiles
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'image', 'user_type','deposite','bio']
