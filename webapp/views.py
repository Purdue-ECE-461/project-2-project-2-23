# Code cited from:
# https://www.django-rest-framework.org/tutorial/quickstart/
# This code is only for testing and learning, and will be deleted finally.

from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.views import TokenObtainPairView
from webapp import serializers

from webapp.serializers import AuthenticationSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes

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

@api_view(['PUT','POST'])
@permission_classes([])
def authenticate(request):
    request.data['username'] = request.data['User']['name']
    request.data['password'] = request.data['Secret']['password']
    try:
        auth_user = User.objects.get(username=request.data['username'])
        if auth_user is not None:
            bearer = RefreshToken.for_user(auth_user)
            bearer_str = ("bearer "+str(bearer.access_token))
            return HttpResponse(bearer_str,status=HTTP_200_OK)
        else:
            return HttpResponse("Invalid authentication request.",status=HTTP_400_BAD_REQUEST)
    except Exception:
        return HttpResponse(HTTP_400_BAD_REQUEST)