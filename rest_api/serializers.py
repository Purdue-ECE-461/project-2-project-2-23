from django.contrib.auth.models import User
from rest_framework import serializers
from rest_api.models import ModuleHistory, ModulePackage, TestApi

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
class HistoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','groups']

class HistoryMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulePackage
        fields = ['Name','Version','ID']
class ModuleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleHistory
        fields = ('user','date','module','action')