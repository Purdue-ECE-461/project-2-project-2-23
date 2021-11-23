from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from rest_api.models import ModulePackage, TestApi
from rest_api.serializers import TestApiSerializer, ModulePackageSerializer
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

@api_view(['GET','DELETE','POST'])
def package_list(request):
    if request.method == 'GET':
        packages = ModulePackage.objects.all()

        content = request.query_params.get('content', None)
        if content is not None:
            packages = packages.filter(title__icontains=content)

        package_serializer = TestApiSerializer(packages,many=True)
        return JsonResponse(package_serializer.data,safe=False)
    elif request.method == 'POST':
        package_data = JSONParser().parse(request)
        package_serializer = ModulePackageSerializer(data=package_data)
        if package_serializer.is_valid():
            package_serializer.save()
            return JsonResponse(package_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(package_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def package_detail(request,pk):
    try:
        package = ModulePackage.objects.get(pk=pk)
    except ModulePackage.DoesNotExist:
        return JsonResponse({'message': 'The package does not exist'}, status=status.HTTP_404_NOT_FOUND,safe=False)

    if request.method == 'GET': 
        package_serializer = ModulePackageSerializer(package) 
        return JsonResponse(package_serializer.data)