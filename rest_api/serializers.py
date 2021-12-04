from rest_framework import serializers
from rest_api.models import ModulePackage, TestApi

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
    Content = serializers.CharField()
    URL = serializers.CharField()
    JSProgram = serializers.CharField()

class PackageCreationSerializer(WritableNestedModelSerializer):
    metadata = PackageMetaSerializer(source='*')
    data = PackageDataSerializer(source='*')

    class Meta:
        model = ModulePackage
        fields = ('metadata','data')
