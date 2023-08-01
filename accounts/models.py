from msilib.schema import ListView
from django.db import models
from django.views.generic import ListView,DetailView
#from .models import Patient_Details

# Create your models here.

class Doctor(models.Model):
    did = models.IntegerField(default=0,max_length=20)
    dname = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField(max_length=100)
    contact= models.IntegerField(max_length=100)
    email = models.EmailField(max_length=100)
    
class Patient_Details(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0,max_length=20)
    place = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    doctor =models.CharField(max_length=100)
    height = models.FloatField(max_length=100, default=0)
    weight = models.FloatField(max_length=100, default=0)
    booked_date = models.DateField(null=True)
    