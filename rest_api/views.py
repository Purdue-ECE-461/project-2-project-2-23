from django.core.checks.messages import Error
import requests
from django.shortcuts import render

from django.http.response import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework import serializers, status

from rest_api.models import ModulePackage, TestApi
from rest_api.serializers import PackageCreationSerializer, TestApiSerializer, ListPackageSerializer
from rest_framework.decorators import api_view

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
        #TODO: Implement version history retreival
        pass
    if request.method == 'DELETE':
        #TODO: Implement deletion by name
        pass
    
# Class-based Views Below:

from django.shortcuts import get_object_or_404
from django.db import IntegrityError
class ModulePackageViewer(ListAPIView):
    queryset = ModulePackage.objects.all()
    serializer_class = ListPackageSerializer #subject to change

    def get(self, request, pk, *args, **kwargs):
        package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
        serializer = PackageCreationSerializer(package)
        return JsonResponse(serializer.data["metadata"], status=status.HTTP_200_OK)
    
    def post(self, request):
        package_serializer = PackageCreationSerializer(data=request.data)
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
