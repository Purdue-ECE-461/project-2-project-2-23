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

# Below are new added serilizers for package change 

# Relating to field:
# "User": {
#       "name": "Paschal Amusuo",
#       "isAdmin": true
#     },

class PackageChangeUserSerializer(serializers.Serializer):
    name = serializers.CharField()
    isAdmin = serializers.BooleanField()

# Relating to field:
# "Date": "2021-11-21T01:11:11Z",

class PackageChangeDateSerializer(serializers.Serializer):
    Date = serializers.CharField()

# Relating to field:
# "PackageMetadata": {
#       "Name": "Underscore",
#       "Version": "1.0.0",
#       "ID": "underscore"
#     },
# No need to create new serializer, using PackageMetaSerializer is OK


# Relating to field:
# "Action": "DOWNLOAD"

class PackageChangeActionSerializer(serializers.Serializer):
    Action = serializers.CharField()


# Nested Serializer

class PackageChangeSerializer(WritableNestedModelSerializer):
    User = PackageChangeUserSerializer(source='*')
    Date = PackageChangeDateSerializer(source='*')
    PackageMetadata = PackageMetaSerializer(source='*')
    Action = PackageChangeActionSerializer(source='*')

    class Meta:
        model = ModulePackage
        fields = ('User','Date','PackageMetadata','Action')


# [
#   {
#     "User": {
#       "name": "Paschal Amusuo",
#       "isAdmin": true
#     },
#     "Date": "2021-11-21T01:11:11Z",
#     "PackageMetadata": {
#       "Name": "Underscore",
#       "Version": "1.0.0",
#       "ID": "underscore"
#     },
#     "Action": "DOWNLOAD"
#   },
#   {
#     "User": {
#       "name": "Paschal Amusuo",
#       "isAdmin": true
#     },
#     "Date": "2021-11-20T01:11:11Z",
#     "PackageMetadata": {
#       "Name": "Underscore",
#       "Version": "1.0.0",
#       "ID": "underscore"
#     },
#     "Action": "UPDATE"
#   },
#   {
#     "User": {
#       "name": "Paschal Amusuo",
#       "isAdmin": true
#     },
#     "Date": "2021-11-19T01:11:11Z",
#     "PackageMetadata": {
#       "Name": "Underscore",
#       "Version": "1.0.0",
#       "ID": "underscore"
#     },
#     "Action": "RATE"
#   },
#   {
#     "User": {
#       "name": "Paschal Amusuo",
#       "isAdmin": true
#     },
#     "Date": "2021-11-18T01:11:11Z",
#     "PackageMetadata": {
#       "Name": "Underscore",
#       "Version": "1.0.0",
#       "ID": "underscore"
#     },
#     "Action": "CREATE"
#   }
# ]
