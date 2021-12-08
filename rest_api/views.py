from django.core.checks.messages import Error
import requests
from django.shortcuts import render

from django.http.response import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework import serializers, status

from rest_api.models import ModuleHistory, ModulePackage, TestApi
from rest_api.serializers import ModuleHistorySerializer, PackageCreationSerializer, TestApiSerializer, ListPackageSerializer
from rest_framework.decorators import action, api_view

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from datetime import datetime

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
    packages_delete = ModulePackage.objects.all().delete()
    tests_deleted = TestApi.objects.all().delete()
    if (packages_delete[0] > 1 and tests_deleted[0] > 1):
        return JsonResponse({'message': 'Registry Reset!'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'message': 'No packages were deleted!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def package_list(request):
    if request.method == 'GET':
        packages = ModulePackage.objects.all()
        package_serializer = ListPackageSerializer(packages,many=True)
        return JsonResponse(package_serializer.data,safe=False)

@api_view(['GET','DELETE'])
def package_by_name(request,pk):
    #TODO: Retreive the package associated with the name of the request (pk)

    if request.method == 'GET':

        change_data = ModuleHistory.objects.filter(User__username=request.user)
        history_serializer = ModuleHistorySerializer(change_data,many=True)
        return JsonResponse(history_serializer.data,status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        #TODO: Implement deletion by name
        pass

class ModuleByNameViewer(ListAPIView):
    queryset = ModulePackage.objects.all()
    serializer_class = ModuleHistorySerializer
    history = ModuleHistory.objects.all()

    def get(self,request,name,*args,**kwargs):
        modules = ModulePackage.objects.filter(Name__startswith=name)
        history = ModuleHistory.objects.all()
        history = history.filter(module__in=modules)
        history_serializer = ModuleHistorySerializer(history,many=True)
        return JsonResponse(history_serializer.data,status=status.HTTP_200_OK,safe=False)
    
    def delete(self,request,name,*args,**kwargs):
        tot_delete = ModulePackage.objects.filter(Name__startswith=name).delete()
        return JsonResponse({'message': '{} Version were deleted successfully!'.format(tot_delete[0])}, status=status.HTTP_200_OK)

class ModulePackageViewer(ListAPIView):
    queryset = ModulePackage.objects.all()
    serializer_class = ListPackageSerializer #subject to change

    def get(self, request, pk=None, *args, **kwargs):
        package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
        history = ModuleHistory.objects.create(user=request.user,date=datetime.now(),module=package,action="DOWNLOAD")
        history.save()
        serializer = PackageCreationSerializer(package)
        return JsonResponse(serializer.data["metadata"], status=status.HTTP_200_OK)
    
    def post(self, request):
        metadata = request.data['metadata']
        if(ModulePackage.objects.filter(ID=metadata['ID']).exists()):
            request.data['metadata']['ID'] = request.data['metadata']['Name']+'-'+request.data['metadata']['Version']
        package_serializer = PackageCreationSerializer(data=request.data)
        # Check if ID is already associated with a model:

        if package_serializer.is_valid():
            try:
                package_serializer.save()
                return JsonResponse(package_serializer.data["metadata"], status=status.HTTP_201_CREATED)
            except IntegrityError:
                return JsonResponse({'message':'Object already exists!'},status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(package_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, *args, **kwargs):
        package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
        if package is not None:
            serializer = PackageCreationSerializer(package,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse(status.HTTP_200_OK)
            return JsonResponse({'message':'failed to update entry.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
        if package is not None:
            package.delete()
            return JsonResponse({'message':'successfully deleted entry.'}, status=status.HTTP_200_OK)
        JsonResponse({'message':'failed to delete entry.'}, status=status.HTTP_400_BAD_REQUEST)
