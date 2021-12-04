from django.db import models

# Create your models here.
class TestApi(models.Model):
    title = models.CharField(max_length=40,blank=False,default='')

class ModulePackage(models.Model):
    Name = models.CharField(max_length=300,blank=False,default='')
    Version = models.CharField(max_length=20,blank=False,default='0.0.0')
    ID = models.CharField(max_length=255,blank=False,primary_key=True)
    Content = models.CharField(max_length=40000000,blank=True)
    URL = models.CharField(max_length=2048,blank=True)
    JSProgram = models.TextField(max_length=10000000,blank=False,default='')