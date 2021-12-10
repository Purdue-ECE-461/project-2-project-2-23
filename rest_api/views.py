from django.core.checks.messages import Error
from django.db.models.expressions import OrderBy
import requests
from django.shortcuts import render

from django.http.response import Http404, HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework import serializers, status

from rest_api.models import ModuleHistory, ModulePackage, ModuleRank, TestApi
from rest_api.serializers import ModuleHistorySerializer, ModuleRankSerializer, PackageCreationSerializer, TestApiSerializer, ListPackageSerializer
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from datetime import datetime
from rest_framework.viewsets import ModelViewSet

from TrustworthyModules.Main import run_rank_mode

from rest_framework.pagination import LimitOffsetPagination

BAD_REQUEST = 'Error, could not find page or user error of api functionality.'

# API Views Below
@api_view(['GET','POST','DELETE'])
def test_list(request):
    if request.method == 'GET':
        tests = TestApi.objects.all()

        title = request.query_params.get('title', None)
        if title is not None:
            tests = tests.filter(title__icontains=title)

        test_serializer = TestApiSerializer(tests,many=True)
        return JsonResponse(test_serializer.data,status=status.HTTP_200_OK,safe=False)
    
    elif request.method == 'POST':
        test_data = JSONParser().parse(request)
        test_serializer = TestApiSerializer(data=test_data)
        if test_serializer.is_valid():
            test_serializer.save()
            return JsonResponse(test_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        tot_delete = TestApi.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(tot_delete[0])}, status=status.HTTP_204_NO_CONTENT, safe=False)

@api_view(['DELETE'])
def reset_registry(request):
    ModuleHistory.objects.all().delete()
    ModulePackage.objects.all().delete()
    TestApi.objects.all().delete()
    ModuleRank.objects.all().delete()
    return HttpResponse(status=status.HTTP_200_OK)
    
def add_history(request,package,action):
    try:
        history = ModuleHistory.objects.create(
                        username=request.user.username,
                        isAdmin=request.user.is_authenticated,
                        date=datetime.now(),
                        module_name=package.Name,
                        module_version=package.Version, 
                        module_ID=package.ID,
                        action=action)
        history.save()
        return
    except Exception:
        print("FAILED TO ADD HISTORY OBJECT TO DATABASE!")
        return

def create_rank(module_name,scores):
    try:
        rank = ModuleRank.objects.create(
            module_id = module_name,
            net_score = scores['NET_SCORE'],
            ramp_up_score = scores['RAMP_UP_SCORE'],
            correctness_score = scores['CORRECTNESS_SCORE'],
            bus_factor_score = scores['BUS_FACTOR_SCORE'],
            responsiveness_score = scores['RESPONSIVENESS_SCORE'],
            dependency_score = scores['DEPENDENCY_SCORE'],
            license_score = scores['LICENSE_SCORE']
        )
        return rank
    except Exception as e:
        print("FAILED TO GENERATE RANK MODEL")
        print(e)
        return None

@api_view(['GET'])
def package_rate(request,pk):
    try:
        package = ModulePackage.objects.get(pk=pk)
        module_rate = ModuleRank.objects.get(module_id=package.ID)
        rate_serializer = ModuleRankSerializer(module_rate)
        return JsonResponse(rate_serializer.data,status=status.HTTP_200_OK)
    except Exception:
        return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def package_list(request):
    try:
        if request.method == 'GET':
            packages = ModulePackage.objects.all()
            package_serializer = ListPackageSerializer(packages,many=True)
            return JsonResponse(package_serializer.data,safe=False)
    except Exception:
        return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

    def get_paginated_response(self, data):
        return Response(data)

class ModuleListViewer(ModelViewSet):
    queryset = ModulePackage.objects.all()
    serializer_class = ListPackageSerializer
    pagination_class = CustomPagination

    def get(self):
        return self.queryset()

class ModuleByNameViewer(ListAPIView):
    queryset = ModulePackage.objects.all().order_by('Name')
    serializer_class = ModuleHistorySerializer
    history = ModuleHistory.objects.all()

    def get(self,request,name,*args,**kwargs):
        try:
            history = ModuleHistory.objects.all()
            history = history.filter(module_name__icontains=name)
            history_serializer = ModuleHistorySerializer(history,many=True)
            return JsonResponse(history_serializer.data,status=status.HTTP_200_OK,safe=False)
        except Exception:
            return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,name,*args,**kwargs):
        try:
            tot_delete = ModulePackage.objects.filter(Name__startswith=name).delete()
            return JsonResponse({'message': '{} Version were deleted successfully!'.format(tot_delete[0])}, status=status.HTTP_200_OK)
        except Exception:
            return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)

class ModulePackageViewer(ListAPIView):
    queryset = ModulePackage.objects.all()
    serializer_class = ListPackageSerializer #subject to change

    def get(self, request, pk=None, *args, **kwargs):
        # Fetch relevant package, update package history
        package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
        add_history(request,package,"DOWNLOAD")
        serializer = PackageCreationSerializer(package)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            # Check if ID is already associated with a model:
            metadata = request.data['metadata']
            rank = None
            if(ModulePackage.objects.filter(ID=metadata['ID']).exists()):
                request.data['metadata']['ID'] = request.data['metadata']['Name']+'-'+request.data['metadata']['Version']

            #
            if('URL' in request.data['data'] and 'Name' in request.data['metadata']):
                # Perform the analysis
                (base64_encode, scores) = run_rank_mode(request.data['data']['URL'])
                rank = create_rank(request.data['metadata']['ID'],scores)
                request.data['data']['Content']=base64_encode

            package_serializer = PackageCreationSerializer(data=request.data)
            # Save package data and update package history associated with module
            if package_serializer.is_valid():
                try:
                    package_serializer.save()
                    if rank is not None:
                        rank.save()
                    package = ModulePackage.objects.get(pk=request.data['metadata']['ID'])
                    add_history(request,package,"CREATED")
                    return JsonResponse(package_serializer.data["metadata"], status=status.HTTP_201_CREATED)
                except IntegrityError:
                    return JsonResponse({'message':'Object already exists!'},status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(package_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
            if package is not None:
                serializer = PackageCreationSerializer(package,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    add_history(request,package,"UPDATED")
                    return HttpResponse(status.HTTP_200_OK)
                return JsonResponse({'message':'failed to update entry.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
            if package is not None:
                add_history(request,package,"DELETED")
                package.delete()
                return JsonResponse({'message':'successfully deleted entry.'}, status=status.HTTP_200_OK)
            JsonResponse({'message':'failed to delete entry.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)
