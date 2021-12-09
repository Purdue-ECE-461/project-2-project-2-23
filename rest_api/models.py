from django.db import models
from django.db.models.fields import CharField, related
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.contrib.auth.models import User

# Create your models here.
class TestApi(models.Model):
    title = models.CharField(max_length=40,blank=False,default='')

class ModulePackage(models.Model):
    Name = models.CharField(max_length=180,blank=False,default='')
    Version = models.CharField(max_length=20,blank=False,default='0.0.0')
    ID = models.CharField(max_length=255,blank=False,primary_key=True)
    Content = models.CharField(max_length=10285760,blank=True,null=True)
    URL = models.CharField(max_length=2048,blank=True,null=True)
    JSProgram = models.TextField(max_length=1000000,blank=False,default='')

class ModuleHistory(models.Model):
    username = models.CharField(max_length=40,blank=True,default='')
    isAdmin = models.BooleanField(blank=True,default=False)
    date = models.DateTimeField(auto_now_add=True,blank=True)
    module_name = models.CharField(max_length=180, blank=False,default='')
    module_version = models.CharField(max_length=20,blank=False,default='')
    module_ID = models.CharField(max_length=255,blank=False,default='')
    action = models.CharField(max_length=20,blank=False,default='')

class ModuleRank(models.Model):
    module_id = models.CharField(max_length=255,blank=False,default='')
    net_score = models.DecimalField(blank=True,max_digits=10,decimal_places=4,default=0.0)
    ramp_up_score = models.DecimalField(blank=True,max_digits=10,decimal_places=4,default=0.0)
    correctness_score = models.DecimalField(blank=True,max_digits=10,decimal_places=4,default=0.0)
    bus_factor_score = models.DecimalField(blank=True,max_digits=10,decimal_places=4,default=0.0)
    responsiveness_score = models.DecimalField(blank=True,max_digits=10,decimal_places=4,default=0.0)
    dependency_score = models.DecimalField(blank=True,max_digits=10,decimal_places=4,default=0.0)
    license_score = models.DecimalField(blank=True,max_digits=10,decimal_places=4,default=0.0)