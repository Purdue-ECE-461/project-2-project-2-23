from django.db import models
from django.db.models.fields import CharField, related
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.contrib.auth.models import User

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

class ModuleHistory(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,blank=True)
    module = ForeignKey(ModulePackage, on_delete=models.CASCADE)
    action = models.CharField(max_length=20,blank=False,default='')

'''
{
    "User": {
      "name": "Paschal Amusuo",
      "isAdmin": true
    },
    "Date": "2021-11-18T01:11:11Z",
    "PackageMetadata": {
      "Name": "Underscore",
      "Version": "1.0.0",
      "ID": "underscore"
    },
    "Action": "CREATE"
  }
  '''