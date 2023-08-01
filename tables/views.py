from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import sqlite3
from accounts.models import Patient_Details,Doctor
from flaskapp.models import Department
#, Patient
from django.db import connection, transaction
from doctor.models import DoctorSchedule
from datetime import date, datetime ,  timedelta, time
from django.utils import timezone
#import datetime
from django.db.models import Q
import time
import dateutil
from dateutil.parser import parse
#from datetime import datetime, timedelta, time




# Create your views here.
subinput = 0
userdatas = {}
maininput = 0
dept_input = 0
doctor_input = 0
todayCount = 0
globelvar={
    'from_number':
    {'subinput':0,
    'userdatas':{},
    'maininput':0,
    'dept_input':0,
    'doctor_input':0,
    'schedule_input':0,
    'doctorId':0,
    'newdoctorId':0,
    'token':0,
    'selected_date':0,
    'duration_per_patient':0,
    'data':0}
}

@csrf_exempt
@twilio_view
def patient_details(request):
    global todayCount
    global globelvar
    pname=""
    age = 0
    department = ""
    doctor=""
    place = ""
    new_id=0
    department_options=""
    i=""
    
    if request.method == 'POST':
        from_number = request.POST.get('From')
        to_number = request.POST.get('To')
        body = request.POST.get('Body').lower()
        response = MessagingResponse()
        resp = response.message()
        respons = ""
        responded = False
        if 'hai' in body or 'hello' in body or "booking" in body or "hi" in body or "morning" in body or "hlo" in body:
            respons = "Good Morning...." \
            "Welcome to MedCare....." \
            "How can i help you..."
            globelvar[from_number]={
                'subinput':0,
                'userdatas':{},
                'maininput':0,
                'dept_input':0,
                'doctor_input':0,
                'schedule_input':0,
                }
            todayCount = Patient_Details.objects.count()
            print(todayCount)
            globelvar[from_number]['maininput'] = 1
            
    

        if globelvar[from_number]['maininput'] == 1:
            if todayCount < 200:
                if globelvar[from_number]['subinput'] == 1:
                    departments = Doctor.objects.values_list('department', flat=True).distinct()
                    department_options = "\n".join([f"{index+1}.{department}" for index, department in enumerate(departments)])
                    if department_options:
                        if body.isdigit():
                            selected_department_index = int(body) - 1
                            if 0 <= selected_department_index < len(departments):
                                globelvar[from_number]['dept_input'] = selected_department_index;
                                department = departments[selected_department_index]
                                globelvar[from_number]['userdatas']['department'] = department
            
                                doctors = Doctor.objects.filter(department=department)
                                doctor_options = "\n".join([f"{index+1}.{doctor.dname}" for index, doctor in enumerate(doctors)])
            
                                respons = f"Please select a doctor in {department}:\n{doctor_options}"
                                responded = True
                                globelvar[from_number]['subinput'] =2;
                            else:
                                respons = "Invalid department selection. Please try again."
                        else:
                            respons = "Please enter a valid department selection."
                    else:
                        respons = "No department options available."
                
                elif globelvar[from_number]['subinput'] == 2:
                    dep = globelvar[from_number]['userdatas']['department']
                    print(dep)
                    doctors1 = Doctor.objects.filter(department=dep)
                    doctor_options = "\n".join([f"{index+1}.{doctor.dname}" for index, doctor in enumerate(doctors1)])

                    if doctor_options:
                        if body.isdigit():
                            selected_doc_index = int(body) - 1
                            if 0 <= selected_doc_index < len(doctors1):
                                globelvar[from_number]['userdatas']['doctor'] = doctors1[selected_doc_index].dname
                                globelvar[from_number]['doctorId'] = doctors1[selected_doc_index].id
                                #globelvar[from_number]['subinput'] = 3
                                

                                # Retrieve the doctor's schedule
                                selected_doctor = doctors1[selected_doc_index]
                                print(selected_doctor)
                                doctor_schedule = DoctorSchedule.objects.filter(doctor=selected_doctor)
                                

                                if doctor_schedule:
                                    today1 = date.today()
                                    today = date(today1.year,today1.month,today1.day)
                                    current_time = datetime.now().time()
                                    print(current_time)
                                    # doctor_schedule = doctor_schedule.filter(
                                    # Q(date__gte=today) | Q(date=today, start_time__gt=current_time)
                                    # )
                                    doctor_schedule = doctor_schedule.filter(
                                     Q(date__gt=today)|Q(date__gte=today, start_time__gt=current_time)
                                    )
                                    # current_time = timezone.now().time()                            
                                    # print(current_time)
                                    print(doctor_schedule)
                                    
                                    respons += f"\nDoctor's Schedule for {selected_doctor.dname}:\n"
                                    for index, schedule in enumerate(doctor_schedule):
                                        
                                        respons += f"{index+1}. Date: {schedule.date}\n   Start Time: {schedule.start_time}\n   End Time: {schedule.end_time}\n"
                                                    
                                        globelvar[from_number]['subinput'] = 3
                                else:
                                    respons += "\nNo schedule available for the selected doctor."
                            else:
                                respons = "Invalid doctor selection. Please try again."
                        else:
                            respons = "Please enter a valid doctor selection."
                    else:
                        respons = "No doctor options available." 
                    
                elif globelvar[from_number]['subinput'] == 3:
                    print(body)
                    today1 = date.today()
                    today = date(today1.year,today1.month,today1.day)
                    current_time = datetime.now().time()
                    doc = globelvar[from_number]['doctorId']
                    doctor_schedule = DoctorSchedule.objects.filter(doctor=doc)
                    doctor_schedule = doctor_schedule.filter(
                        Q(date__gt=today)|Q(date__gte=today, start_time__gt=current_time)
                    )
                    # current_date = datetime.now().date()
                    # selected_date = globelvar[from_number]['selected_date']
                    
                    schedule_options = "\n".join([f"{index+1}.{schedule.date}" for index, schedule in enumerate(doctor_schedule)])
                    if schedule_options:
                        if body.isdigit():
                            selected_schedule_index = int(body) - 1
                            if 0 <= selected_schedule_index < len(doctor_schedule):
                                globelvar[from_number]['selected_date'] = doctor_schedule[selected_schedule_index].date
                                print('selected shedule date is')
                                print(globelvar[from_number]['selected_date'])
                            else:
                                        # The user did not enter a valid schedule selection
                                    selected_schedule_index = -1
                        else:
                            # The user did not enter a valid schedule selection
                            selected_schedule_index = -1

                        if selected_schedule_index == -1:
                            respons = "Please enter a valid schedule selection."
                        else:
                            if doctor_schedule[selected_schedule_index].on_leave:
                                    # If the doctor is on leave, send a message to the patient
                                respons = "Sorry, the doctor is on leave on the selected date. Please choose another date."
                                globelvar[from_number]['subinput'] = 2  # Go back to selecting the doctor
                            else:
                                # If the doctor is available, proceed with booking      
                                for doc_schedule in doctor_schedule:
                                    if doc_schedule.date == globelvar[from_number]['selected_date']:
                                        patient_limit = doc_schedule.limit
                                        print("Doctor:", doc_schedule.doctor.dname)
                                        print("Date:", doc_schedule.date)
                                        print("Patient Limit:", patient_limit)
                                        start_time = doc_schedule.start_time  
                                        globelvar[from_number]['duration_per_patient']= start_time# Assuming start_time is a valid datetime object
                                        end_time = doc_schedule.end_time 
                                        
                                
                                #print(add_minutes(start_time,5))
                                

                                #print("Original Time:", start_time)
                                # print("Updated Time (after adding 5 minutes):",updated_time)
                                data = Patient_Details.objects.filter(doctor=doc_schedule.doctor.dname, booked_date=globelvar[from_number]['selected_date']).count()
                                print("Number of patients booked for the selected date:", data)
                                globelvar[from_number]['data'] = data
                                if data >= patient_limit:
                                    respons = "Today's appointment slots are full. Please select another date."
                                    # Reset the subinput after displaying the message
                                    globelvar[from_number]['subinput'] = 0
                                    
                                    
                                else:
                                    globelvar[from_number]['userdatas']['booked_date'] = globelvar[from_number]['selected_date']
                                    
                                    
                                    time_difference = timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second) - \
                                    timedelta(hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second)

                                    # Calculate the total seconds in the time difference
                                    total_seconds = time_difference.total_seconds()
                                    
                                    onePatientSeconds = total_seconds/patient_limit;
                                    
                                    new_datetime = datetime.combine(date.today(),start_time)+timedelta(seconds=(onePatientSeconds*data))
                                    # new_datetime = globelvar[from_number]['duration_per_patient'] + timedelta(minutes=5)

                                    # Extract the time component from the updated datetime object
                                    updated_time = new_datetime.time()
                                    globelvar[from_number]['duration_per_patient']=updated_time
                                    print('updated time is',updated_time)
                                    respons = "Please enter your name"
                                    globelvar[from_number]['subinput']+=1
                    
                elif globelvar[from_number]['subinput'] == 4:
                    pname = body
                    print(pname)
                    globelvar[from_number]['userdatas']['name'] = pname
                    respons = "Please enter your age"
                   
                    globelvar[from_number]['subinput'] = globelvar[from_number]['subinput']+1
                elif globelvar[from_number]['subinput'] == 5:
                    age = body
                    print(age)
                    globelvar[from_number]['userdatas']['age'] = age
                    respons = "Please enter your place"
                   
                    globelvar[from_number]['subinput'] = globelvar[from_number]['subinput']+1
                elif globelvar[from_number]['subinput'] == 6:
                    place = body
                    globelvar[from_number]['userdatas']['place'] = place
                    
                    #respons = "Thanks for entering your place....Booking Completed\nYour token number is "
                   
                    dict_data = Patient_Details(**globelvar[from_number]['userdatas'])
                    dict_data.save()
                    #print("ID:", dict_data.id)
                    token = globelvar[from_number]['data']
                    patient_time = globelvar[from_number]['duration_per_patient']
                    respons = "Booking Completed\nYour token number is  %d \nThis is your patient id for further use. ID: %d\nYou have to reach clinic  %s"%(token,dict_data.id,patient_time)
                   
                    globelvar[from_number]['subinput'] = globelvar[from_number]['subinput']+1
                            
                    

                if 'booking' in body or 'book' in body or 'appointment' in body or 'consult' in body:
                    departments = Doctor.objects.values_list('department', flat=True).distinct()
                    department_options = "\n".join([f"{index+1}.{department}" for index, department in enumerate(departments)])
                    print(department_options)
                    respons = f"Please select a department:\n{department_options}"
                    globelvar[from_number]['subinput'] = 1
                    
                # Add the reschedule trigger to check for 'reschedule' in the user's message body
                if 'reschedule' in body:
                    respons = "Please enter your token number (patient ID) to proceed with rescheduling:"
                    globelvar[from_number]['subinput'] = 9

                # ... (existing code)

                elif globelvar[from_number]['subinput'] == 9:
                    # User is in the process of rescheduling, capture the token number
                    token_number = body

                    # Retrieve the appointment record for the specified token number
                    try:
                        token_number = int(body)
                        globelvar[from_number]['token']=token_number 
                        appointment = Patient_Details.objects.get(id=token_number)
                        booked_date = appointment.booked_date
                        doctor = appointment.doctor
                        doc = Doctor.objects.get(dname=doctor)
                        doc_id = doc.id
                        globelvar[from_number]['newdoctorId']= doc_id
                        print(doc_id)
                        print(doctor)
                        doctor_schedule = DoctorSchedule.objects.filter(doctor=doc)

                        if date.today() <= booked_date:
                            if doctor_schedule:
                                today = date.today()
                                respons += f"\nDoctor's Schedule for Dr.{doctor}:\n"
                                for index, schedule in enumerate(doctor_schedule):
                                    if schedule.date >= today: 
                                        respons += f"{index+1}. Date: {schedule.date}\n   Start Time: {schedule.start_time}\n   End Time: {schedule.end_time}\n"
                                        
                                    
                            # The appointment is scheduled for a future date, so it can be rescheduled
                            #respons = "Please enter the new date for the appointment (YYYY-MM-DD):"
                            globelvar[from_number]['subinput'] = 10
                        else:
                            # The appointment is for today or a past date, it cannot be rescheduled
                            respons = "Sorry, you cannot reschedule an appointment for today or a past date."

                    except Patient_Details.DoesNotExist:
                        # The token number doesn't exist in the database
                        respons = "Invalid token number. Please enter a valid token number for rescheduling."

                # ... (existing code)
                    
                elif globelvar[from_number]['subinput'] == 10:
                    print(body)
                    doc = globelvar[from_number]['newdoctorId']
                    token = globelvar[from_number]['token']
                    print(str(doc)+' sample')
                    
                    doctor_schedule = DoctorSchedule.objects.filter(doctor=doc)
                    schedule_options = "\n".join([f"{index+1}.{schedule.date}" for index, schedule in enumerate(doctor_schedule)])
                    print(schedule_options)
                    
                    if schedule_options:
                        if body.isdigit():
                            selected_schedule_index = int(body) - 1
                            if 0 <= selected_schedule_index < len(doctor_schedule):
                                new_date= doctor_schedule[selected_schedule_index].date
                                Patient_Details.objects.filter(id=token).update(booked_date=new_date)
    
                                selected_schedule = doctor_schedule[selected_schedule_index]
                            else:
                                # The user did not enter a valid schedule selection
                                selected_schedule_index = -1
                        else:
                            # The user did not enter a valid schedule selection
                            selected_schedule_index = -1

                        if selected_schedule_index == -1:
                            respons = "Please enter a valid schedule selection."
                        else:
                            if selected_schedule.on_leave:
                                    # If the doctor is on leave, send a message to the patient
                                respons = "Sorry, the doctor is on leave on the selected date. Please choose another date."
                                globelvar[from_number]['subinput'] = 2  # Go back to selecting the doctor
                            else:
                                # If the doctor is available, proceed with booking
                                respons = f"Your appointment has been rescheduled to {new_date}."
                                globelvar[from_number]['subinput'] += 0
    
                if 'cancel' in body:
                    respons = "Please enter your token number (patient ID) to proceed with the cancellation:"
                    globelvar[from_number]['subinput'] = 11



                elif globelvar[from_number]['subinput'] == 11:
    
                    token_number = body

                    try:
                        token_number = int(body)
                        # Check if the token number exists in the database
                        appointment = Patient_Details.objects.get(id=token_number)
                        
                        # Delete the appointment record for the specified token number
                        appointment.delete()
                        respons = "Your appointment has been successfully canceled."
                        
                    except Patient_Details.DoesNotExist:
                        # The token number doesn't exist in the database
                        respons = "Invalid token number. Please enter a valid token number for cancellation."
                    except Exception as e:
                        # Handle any other potential errors during the cancellation process
                        respons = "An error occurred during cancellation. Please try again later."

                    # Reset the subinput after the cancellation process
                    globelvar[from_number]['subinput'] = 0    
                        
                # if body == "cancel":
                #     respons = "Your appointment is canceled."

                #     cursor = connection.cursor()
                #     query = f"DELETE FROM Patient_Details WHERE phone_number=globelvar[from_number]"
                #     print(query)  # Check the printed query in the console
                #     cursor.execute(query)
                #     connection.commit()
               
            
        if globelvar[from_number]['subinput'] == 7:
            globelvar[from_number]['maininput'] = 0
            globelvar[from_number]['subinput'] = 0
            globelvar[from_number]['dept_input'] = 0
            globelvar[from_number]['doctor_input'] = 0

        print(respons)
        print(userdatas)
        
        
        account_sid = 'ACb11063994a625678d16cbf3b5fd91995'
        auth_token = 'c3c7c89fbc25f6eb18d614cc0e361702'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=respons, from_=to_number, to=from_number)
    return HttpResponse(str(resp))

def execute(self, query):
    """Executes the given query."""
    cursor = connection.cursor()
    cursor.execute(query.replace(":", "?"))
    return cursor



def add_minutes(time, minutes):
  

  time_obj = datetime.datetime.strptime(time, "%H.%M.%S")
  new_time_obj = time_obj + datetime.timedelta(minutes=minutes)
  new_time = new_time_obj.strftime("%H.%M.%S")
  return new_time