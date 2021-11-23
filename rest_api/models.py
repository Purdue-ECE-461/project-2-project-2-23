from django.db import models

# Create your models here.
class TestApi(models.Model):
    title = models.CharField(max_length=40,blank=False,default='')

class ModulePackage(models.Model):
    name = models.CharField(max_length=300,blank=False,default='')
    version = models.CharField(max_length=20,blank=False,default='0.0.0')
    content = models.CharField(max_length=40000000,blank=False,default='')