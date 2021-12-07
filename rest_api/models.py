from django.db import models

# Create your models here.
class TestApi(models.Model):
    title = models.CharField(max_length=40,blank=False,default='')

class ModulePackage(models.Model):
    Name = models.CharField(max_length=300,blank=False,default='')
    Version = models.CharField(max_length=20,blank=False,default='0.0.0')
    ID = models.CharField(max_length=255,blank=False,primary_key=True)
    Content = models.CharField(max_length=10285760,blank=True,null=True)
    URL = models.CharField(max_length=2048,blank=True,null=True)
    JSProgram = models.TextField(max_length=1000000,blank=False,default='')


# class ModuleChange(models.Model):
#     # Could point to the actual model, don't know yet

#     User = models.CharFiled(max_length=300,blank=False,default='')# A
#     # name = models.CharFiled(max_length=300,blank=False,default='')
#     # isAdmin = models.BooleanField(max_length=10,blank=False)

#     Date = models.ChaFiled(max_length=100,blank=False,default='')
#     changePackage = models.charField(max_length=300,blank=False,default='') # A
#     # Name = models.CharField(max_length=300,blank=False,default='')
#     # Version = models.CharField(max_length=20,blank=False,default='0.0.0')
#     # ID = models.CharField(max_length=255,blank=False,primary_key=True)
#     Action = models.ChaFiled(ma_length=20,blank=False,default='')






# New modeled needed 
# Example return body

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