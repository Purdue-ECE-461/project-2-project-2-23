from django.contrib.auth.models import User
from rest_framework import serializers
from rest_api.models import ModuleHistory, ModulePackage, ModuleRank, TestApi

from drf_writable_nested.serializers import WritableNestedModelSerializer

class TestApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestApi
        fields = ('id','title')

class ListPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulePackage
        fields = ('Name', 'Version', 'ID')

class PackageMetaSerializer(serializers.Serializer):
    Name = serializers.CharField()
    Version = serializers.CharField()
    ID = serializers.CharField()

class PackageDataSerializer(serializers.Serializer):
    Content = serializers.CharField(required=False,default='')
    URL = serializers.CharField(required=False,default='')
    JSProgram = serializers.CharField()

class PackageCreationSerializer(WritableNestedModelSerializer):
    metadata = PackageMetaSerializer(source='*')
    data = PackageDataSerializer(source='*')

    class Meta:
        model = ModulePackage
        fields = ('metadata','data')
class HistoryUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    isAdmin = serializers.BooleanField()

class HistoryMetaSerializer(serializers.Serializer):
    module_name = serializers.CharField()
    module_version = serializers.CharField()
    module_ID = serializers.CharField()
class ModuleHistorySerializer(WritableNestedModelSerializer):
    User = HistoryUserSerializer(source='*')
    PackageMetaData = HistoryMetaSerializer(source='*')
    class Meta:
        model = ModuleHistory
        fields = ('User','date','PackageMetaData','action')

class ModuleRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleRank
        fields = ('net_score','ramp_up_score', 'correctness_score','bus_factor_score','responsiveness_score','dependency_score','license_score')