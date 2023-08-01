from django.db import models
from accounts.models import Patient_Details,Doctor
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class History(models.Model):
    p_id = models.ForeignKey(Patient_Details,on_delete=models.CASCADE)
    symptoms = models.TextField(max_length=200)
    tests = models.TextField(max_length=200)
    advice = models.TextField(max_length=200)
    medicine = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True,null=True)





class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='doctor_schedules')
    dep=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='department_schedules',null=True)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()
    on_leave = models.BooleanField(default=False,null=True)
    limit = models.IntegerField(max_length=100, null=True)
    appointment_count = models.PositiveIntegerField(default=0)  # Initialize appointment count to 0


    def __str__(self):
        return f"Schedule for {self.doctor.dname} on {self.date}"
    
   



class Appointment(models.Model):
    dept =models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='department_appointment',null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='doctor_appointment')
    patient = models.ForeignKey(Patient_Details, on_delete=models.CASCADE)
    appointment_date = models.ForeignKey( DoctorSchedule, on_delete=models.CASCADE,related_name='appointments_date')
    

    def __str__(self):
        return f"Appointment for {self.doctor.dname} with {self.patient.name}"
    