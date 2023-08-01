from audioop import reverse
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from django_twilio.decorators import twilio_view
from .models import Department,schedule
from accounts.models import Doctor,Patient_Details
from bot.models import department_list
from django.urls import reverse
from django.http import HttpRequest,HttpResponseRedirect
from tables.forms import MyForm
from django import forms
from django.contrib import messages
from doctor.models import DoctorSchedule

#from .views import admin_home_view

#123from flaskapp import app

# Create your views here.

maininput=0
dept=0
doctor=0


@csrf_exempt
@twilio_view
def chatbot(request):
    global maininput
    global dept
    global doctor
    if request.method == 'POST':
        incoming_msg = request.POST.get('Body', '').lower()
        recieverPhoneNo = request.POST.get('From', '')
        response = MessagingResponse()
        resp = response.message()
        respons=""
        
        if  'hi' in incoming_msg:
            respons  = "how can i help you?"
            maininput=1
        if maininput==1:
            if 'book' in incoming_msg:
                respons = "department"
                dept=1
                if dept==1 and 'pediatrician' in incoming_msg:
                    respons="doctor"
                    doctor=1
                    if doctor==1:
                        respons="name?"
                        doctor=doctor+1
                    elif doctor==2:
                        respons="place"
                        doctor=doctor+1
                    elif doctor==3:
                        respons="age"
                        doctor=doctor+1
        else:
            respons="Todays booking closed"    
            
            
        account_sid = 'ACb828895438c99ae4a1a89cbc8faa2096'
        auth_token = 'f95011ad947de9a307b719a17c7cf87f'
        client= Client(account_sid,auth_token)
        message = client.messages.create(body=respons,
                    from_='whatsapp:+14155238886',
                    to=recieverPhoneNo
                    )

    print(message.sid)
    print(incoming_msg)
    print(recieverPhoneNo)
    
    
    return HttpResponse(str(resp))


def admin_home_view(request):
    
    #return render(request,'admin_temp/pages/examples/adminindex.html')
    return render(request,'admin_temp/pages/examples/adminindex.html')


def departments(request):
    dept = Department.object.values()
    print(dept)
    
    return render(request,'admin_temp/pages/examples/blank.html')


def admin_view_patients(request):
    data = Patient_Details.objects.all()

    return render(request,'admin_temp/pages/examples/admin_view_patients.html', {'data': data})


def admin_view_appointments(request):
    data = Patient_Details.objects.all()
    return render(request,'admin_temp/pages/examples/admin_view_appointment.html', {'data': data})

def admin_add_appointments(request):
    return render(request,'admin_temp/pages/examples/admin_add_appointments.html')

# def admin_view_history(request):
#     return render(request,'admin_temp/pages/examples/admin_view_history.html')



def admin_view_doctors(request):
    doc = Doctor.objects.all()
    return render(request, 'admin_temp/pages/examples/admin_view_doctors.html', {'doc': doc})




def admin_view_department(request):
    #doc = Doctor.objects.all()
    doc = department_list.objects.all()
    return render(request, 'admin_temp/pages/examples/admin_view_department.html', {'doc': doc})

def delete(request, pid):
    # Get the record to delete
    record = Patient_Details.objects.get(id=pid)

    # Delete the record
    record.delete()

    # Redirect the user back to the index view
    return redirect('admin_view_patients')



def admin_update_patient(request, pid):
    patient = Patient_Details.objects.get(id=pid)
    patient.name=request.POST['name']
    patient.age=request.POST['age']
    patient.place=request.POST['place']
    patient.height=request.POST['height']
    patient.weight=request.POST['weight']
    patient.save()
    messages.info(request,"ITEM UPDATED SUCCESSFULLY")
    return redirect('admin_view_patients')

def admin_update_doctor(request,pid):
    doctor = Doctor.objects.get(id=pid)
    doctor.dname = request.POST['dname']
    doctor.department =request.POST['department']
    doctor.qualification =request.POST['qualification']
    doctor.experience =request.POST['experience']
    doctor.email =request.POST['email']
    doctor.contact =request.POST['contact']
    doctor.save()
    return redirect('admin_view_doctors')
    
    

def edit_item(request,pid):
    edit = Patient_Details.objects.get(id=pid)
    data = Patient_Details.objects.all()
    context={
        'edit':edit,
        'data':data
    }
    return render(request, 'admin_temp/pages/examples/admin_edit_patient.html',context)


def add_item(request):
    # dept = Doctor.objects.values('department').distinct()
    # doc = Doctor.objects.values('dname').distinct()
    doc = Doctor.objects.values('dname','department').distinct()
    if request.method=="POST":
        department=request.POST['department']
        doctor=request.POST['doctor']
        name=request.POST['name']
        age=request.POST['age']
        place=request.POST['place']
        height=request.POST['height']
        weight=request.POST['weight']
        item=Patient_Details(name=name,age=age,place=place,height=height,weight=weight,department=department,doctor=doctor)
        item.save()
        messages.info(request,"ITEM ADDED SUCCESSFULLY")
    
    
    item_list=Patient_Details.objects.all()
    context={
        'item_list':item_list,
        'doc':doc,
        'dept':dept
    }
    
    return render(request, 'admin_temp/pages/examples/admin_update_patient.html', context)


def add_dept(request):
    if request.method=="POST":
        dept_id=request.POST['id']
        department=request.POST['department']
        dept = department_list(dname=department,dept_id=dept_id)
        dept.save()
    return render(request, 'admin_temp/pages/examples/add_department.html')

def schedule(request):
   # doc=Doctor.objects.get(id=did)
    if request.method=="POST": 
        on_leave=request.POST.get('on_leave')
        if on_leave == 'on':
            on_leave = True
        else:
            on_leave = False
        scheduledate=request.POST['scheduledate']
        starttime=request.POST['starttime']
        endtime=request.POST['endtime']
        limit = request.POST['points']
        print(scheduledate,starttime,endtime)
        doctor_name = request.POST.get('doctor')
        doctor = Doctor.objects.filter(dname=doctor_name).first()
        item=DoctorSchedule(doctor=doctor,date=scheduledate,start_time=starttime,end_time=endtime,on_leave=on_leave, limit = limit)
        item.save()
    context={
        'item':item,
        #'doc':doc
    }
    return render(request, 'admin_temp/pages/examples/admin_schedule.html',context)

def view_schedule(request,did):
    doc=Doctor.objects.filter(id=did)
    
    context={
        'doc':doc
    }
    return render(request, 'admin_temp/pages/examples/admin_schedule.html',context)

def edit_doctor_item(request,pid):
    edit = Doctor.objects.get(id=pid)
    data = Doctor.objects.all()
    context={
        'edit':edit,
        'data':data
    }
    return render(request, 'admin_temp/pages/examples/admin_edit_doctor.html',context)