from dataclasses import fields
from rest_framework.serializers import ModelSerializer

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from api.models import Profile, Referral

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email","password","id"]
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data) 
        
class ReferralSerializer(ModelSerializer):
    class Meta:
        model = Referral
        fields = "__all__"
        
class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"