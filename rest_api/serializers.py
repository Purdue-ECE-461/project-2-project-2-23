from rest_framework import serializers
from rest_api.models import ModulePackage, TestApi

class TestApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestApi
        fields = ('id','title')

class ModulePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulePackage
        fields = ('name','id', 'version')