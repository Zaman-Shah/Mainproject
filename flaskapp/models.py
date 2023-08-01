from django.db import models
from django import forms

# Create your models here.

class Department(forms.Form):
    dept_id = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
class schedule(models.Model):
    scheduledate= models.DateField()
    starttime=models.TimeField()
    endtime=models.TimeField()

    def __str__(self):
        return 

    def __unicode__(self):
        return 
