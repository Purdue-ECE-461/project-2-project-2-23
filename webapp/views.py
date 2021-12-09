# Code cited from:
# https://www.django-rest-framework.org/tutorial/quickstart/
# This code is only for testing and learning, and will be deleted finally.

from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.views import TokenObtainPairView
from webapp import serializers

from webapp.serializers import AuthenticationSerializer, UserSerializer

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth import authenticate

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = AuthenticationSerializer