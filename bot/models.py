from django.db import models
from django.utils.timezone import timezone
from datetime import datetime 
from django.utils import timezone
# Create your models here.

# class Patient(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField(default=0,max_length=20)
#     place = models.CharField(max_length=100)
#     department = models.CharField(default=str(True) , max_length=100)
#     doctor =models.CharField(default=str(True) ,max_length=100)
#     height = models.FloatField(max_length=100, default=str(True))
#     weight = models.FloatField(max_length=100, default=str(True))
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         db_table = 'patient'
    
    
    
    
class WhatsAppMessage(models.Model):
    from_number = models.CharField(max_length=20)
    to_number = models.CharField(max_length=20)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class department_list(models.Model):
    dept_id = models.IntegerField()
    dname = models.CharField(max_length=100)    
    
    def __str__(self):
        return self.dname
