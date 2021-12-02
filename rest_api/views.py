from django.core.checks.messages import Error
import requests
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework import serializers, status

from rest_api.models import ModulePackage, TestApi
from rest_api.serializers import TestApiSerializer, ListPackageSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET','POST','DELETE'])
def test_list(request):
    if request.method == 'GET':
        tests = TestApi.objects.all()

        title = request.query_params.get('title', None)
        if title is not None:
            tests = tests.filter(title__icontains=title)

        test_serializer = TestApiSerializer(tests,many=True)
        return JsonResponse(test_serializer.data,safe=False)
    
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
    if (packages_delete[0] > 1):
        return JsonResponse({'message': 'Registry Reset!'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'message': 'No packages were deleted!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def package_list(request):
    if request.method == 'GET':
        packages = ModulePackage.objects.all()
        package_serializer = ListPackageSerializer(packages,many=True)
        return JsonResponse(package_serializer.data,safe=False)

from django.shortcuts import get_object_or_404
class ModulePackageViewer(ListAPIView):
    queryset = ModulePackage.objects.all()
    serializer_class = ListPackageSerializer #subject to change

    def get(self, request, pk, *args, **kwargs):
        package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
        serializer = ListPackageSerializer(package)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        package_data = JSONParser().parse(request)
        package_serializer = ListPackageSerializer(data=package_data)
        if package_serializer.is_valid():
            package_serializer.save()
            return JsonResponse(package_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(package_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, *args, **kwargs):
        package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
        if package is not None:
            serializer = ListPackageSerializer(package,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=status.HTTP_200_OK)
            return JsonResponse({'message':'failed to update entry.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
        if package is not None:
            package.delete()
            return JsonResponse({'message':'successfully deleted entry.'}, status=status.HTTP_200_OK)
        JsonResponse({'message':'failed to delete entry.'}, status=status.HTTP_400_BAD_REQUEST)

'''
@api_view(['GET','POST','PUT','DELETE'])
def package_detail(request):
    # get ID,Name,Version
    # check if ID,Name, and Version are already in objects
    print(request)

    if request.method == 'POST':
            package_data = JSONParser().parse(request)
            package_serializer = ListPackageSerializer(data=package_data)
            if package_serializer.is_valid():
                package_serializer.save()
                return JsonResponse(package_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(package_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET': 
        pk
        package = get_object_or_404(ModulePackage,ID=)

        package_serializer = ListPackageSerializer(package,many=False)
        return JsonResponse(package_serializer.data,safe=False)
    if request.method == 'PUT':
        #get the specific object
        # update fields
        # send some reply
        #save on database
        pass
'''