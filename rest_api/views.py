import queue
from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework import serializers, status

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from rest_api.models import ModuleHistory, ModulePackage, ModuleRank, TestApi
from rest_api.serializers import ModuleHistorySerializer, ModuleRankSerializer, PackageCreationSerializer, TestApiSerializer, ListPackageSerializer
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from datetime import datetime
from rest_framework.viewsets import ModelViewSet

from TrustworthyModules.Main import run_rank_mode

from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
import threading
from queue import Queue

BAD_REQUEST = 'Error, could not find page or user error of api functionality.'

# Helper functions + classes
def ez_logger(source,info):
    log_time = datetime.now().strftime("%H:%M:%S")
    print("[INFO][%s] \"%s\":  %s" % (log_time,source,info))

class CustomPagination(PageNumberPagination):
    page_size=10
    page_query_param='offset'

    def get_paginated_response(self, data):
        return Response(data)

    
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
        ez_logger("ADD_HISTORY","FAILED TO UPDATE HISTORY")
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
        ez_logger("CREATE_RANK","FAILED TO RATE THE MODULE")
        return None


# API Views

@api_view(['DELETE'])
def reset_registry(request):
    ez_logger("/reset","resetting registry...")
    ModuleHistory.objects.all().delete()
    ModulePackage.objects.all().delete()
    TestApi.objects.all().delete()
    ModuleRank.objects.all().delete()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['GET'])
def package_rate(request,pk):
    ez_logger("PACKAGE_RATE",request.data)
    try:
        package = ModulePackage.objects.get(pk=pk)
        add_history(request,package,"RATE")
        if package.URL == '':
            return HttpResponseBadRequest("Cannot call rate on packages with no linked repository!")
        else:
            try:
                module_rate = ModuleRank.objects.get(module_id__icontains=package.ID)
            except ModuleRank.DoesNotExist:
                 return HttpResponse("Could not rate the package (Github Token Usage or Timeout Exceeded)",
                 status=status.HTTP_400_BAD_REQUEST)
            rate_serializer = ModuleRankSerializer(module_rate)
            return JsonResponse(rate_serializer.data,status=status.HTTP_200_OK)
    except Exception:
        err_str = "FAILURE OCCURED, EXCEPTION %s" % str(Exception)
        ez_logger("PACKAGE_RATE",err_str)
        return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)


class ModuleListViewer(ModelViewSet):
    queryset = ModulePackage.objects.all().order_by('Name')
    serializer_class = ListPackageSerializer
    pagination_class = CustomPagination

    def get(self):
        ez_logger("GET /packages","DEPRECATE THIS METHOD")
        return self.queryset()

    def post(self, request):
        ez_logger("POST /packages",request.data)
        ret_query = []
        for query in request.data:
            q = ModulePackage.objects.all().filter(Name__icontains=query['Name']).values('Name','ID','Version')
            ret_query.append(q)
        ret_list = ret_query[0]
        for qs in ret_query:
            ret_list = ret_list.union(qs)
        return JsonResponse(list(ret_list),safe=False,status=status.HTTP_200_OK)

class ModuleByNameViewer(ListAPIView):
    queryset = ModulePackage.objects.all().order_by('Name')
    serializer_class = ModuleHistorySerializer
    history = ModuleHistory.objects.all()

    def get(self,request,name,*args,**kwargs):
        ez_logger(("GET /package/%s" % name),request.data)
        try:
            history = ModuleHistory.objects.all()
            history = history.filter(module_name__icontains=name)
            history_serializer = ModuleHistorySerializer(history,many=True)
            return JsonResponse(history_serializer.data,status=status.HTTP_200_OK,safe=False)
        except Exception:
            return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,name,*args,**kwargs):
        ez_logger(("GET /package/%s" % name),request.data)
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
        ez_logger(("GET /package/%s" % pk),request.data)
        package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
        add_history(request,package,"DOWNLOAD")
        serializer = PackageCreationSerializer(package)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Check if ID is already associated with a model:
        ez_logger(("POST /package"),request.data)
        metadata = request.data['metadata']
        rank = None
        if(ModulePackage.objects.filter(ID=metadata['ID']).exists()):
            request.data['metadata']['ID'] = request.data['metadata']['Name']+'-'+request.data['metadata']['Version']
        #
        if('URL' in request.data['data'] and 'ID' in request.data['metadata']):
            ez_logger(("POST /package"),"PACKAGE INGESTION RUNNING")
            # Perform the analysis
            (base64_encode, scores) = run_rank_mode(request.data['data']['URL']) # this was original line
            rank = create_rank(request.data['metadata']['ID'],scores)
            request.data['data']['Content']=base64_encode
        else:
            ez_logger(("POST /package"),"REGULAR PACKAGE UPLOAD")
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
    
    def put(self, request, pk, *args, **kwargs):
        try:
            ez_logger(("GET /package/%s" % pk),request.data)
            package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
            if package is not None:
                if('URL' in request.data['data'] and request.data['data']['URL'] != package.URL):
                    (base64_encode, scores) = run_rank_mode(request.data['data']['URL'])
                    rank = create_rank(package.Name,scores)
                    rank.save()
                    request.data['data']['Content'] = base64_encode
                else:
                    print("CONTENT CHANGE")
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
            ez_logger(("GET /package/%s" % pk),request.data)
            package = get_object_or_404(ModulePackage,ID=self.kwargs.get('pk'))
            if package is not None:
                add_history(request,package,"DELETED")
                package.delete()
                return JsonResponse({'message':'successfully deleted entry.'}, status=status.HTTP_200_OK)
            JsonResponse({'message':'failed to delete entry.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return HttpResponse(BAD_REQUEST,status=status.HTTP_404_NOT_FOUND)
