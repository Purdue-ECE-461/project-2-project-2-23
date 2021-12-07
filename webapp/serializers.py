# Code cited from:
# https://www.django-rest-framework.org/tutorial/quickstart/
# This code is only for testing and learning, and will be deleted finally.

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class AuthenticationSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        ret_data['token'] = data['access']
        return ret_data

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']