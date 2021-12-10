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
        ordering = ['-id']
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
    name = serializers.CharField(source='username')
    isAdmin = serializers.BooleanField()

class HistoryMetaSerializer(serializers.Serializer):
    Name = serializers.CharField(source='module_name')
    Version = serializers.CharField(source='module_version')
    ID = serializers.CharField(source='module_ID')

class ModuleHistorySerializer(WritableNestedModelSerializer):
    User = HistoryUserSerializer(source='*')
    PackageMetadata = HistoryMetaSerializer(source='*')
    Date = serializers.CharField(source='date')
    Action = serializers.CharField(source='action')
    class Meta:
        model = ModuleHistory
        fields = ('User','Date','PackageMetadata','Action')

class ModuleRankSerializer(serializers.ModelSerializer):
    RampUp = serializers.DecimalField(max_digits=10,decimal_places=2,source='ramp_up_score')
    Correctness = serializers.DecimalField(max_digits=10,decimal_places=2,source='correctness_score')
    BusFactor = serializers.DecimalField(max_digits=10,decimal_places=2,source='bus_factor_score')
    ResponsiveMaintainer = serializers.DecimalField(max_digits=10,decimal_places=2,source='responsiveness_score')
    LicenseScore = serializers.DecimalField(max_digits=10,decimal_places=2,source='license_score')
    GoodPinningPractice = serializers.DecimalField(max_digits=10,decimal_places=2,source='dependency_score')
    class Meta:
        model = ModuleRank
        fields = (
            'RampUp',
            'Correctness',
            'BusFactor',
            'ResponsiveMaintainer',
            'LicenseScore',
            'GoodPinningPractice'
        )