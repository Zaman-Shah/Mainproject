from django.shortcuts import render ,redirect
from accounts.models import Patient_Details,Doctor
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import History,DoctorSchedule,Appointment
from datetime import date

# Create your views here.

def doctor_home_view(request):
    
    return render(request,'doctor/doctor_home.html')

# def prescription(request):
#     data = Patient_Details.objects.all()
#     return render(request, 'doctor/prescription.html', {'data': data})

@login_required
def doctor_view_appointment(request):
    username = request.user.username
    print(username)
    

    # Retrieve the patients associated with the specific doctor
    patients = Patient_Details.objects.filter(doctor=username)

    # Pass the patient data to the template
    
    return render(request, 'doctor/doctor_view_appointment.html', {'patients': patients})

def doctor_view_patient(request):
    data = Patient_Details.objects.filter()
    return render(request, 'doctor/doctor_view_patient.html', {'data': data})


def doctor_view_history(request, pid):
    new = Patient_Details.objects.get(id=pid)
    data = Patient_Details.objects.values()
    items = History.objects.filter(p_id_id=new)
    context = {
        'items': items,
        'new': new,
        'data': data
    }
    return render(request, 'doctor/doctor_view_history.html',context)



# def doctor_view(request):
#     # Get the specific doctor's ID from the request parameters or session
#     doctor_id = request.GET.get('doctor_id')

#     # Retrieve the patients associated with the specific doctor
#     patients = Patient_Details.objects.filter(doctor=doctor_id)

#     # Pass the patient data to the template
#     context = {'data': patients}
#     return render(request, 'doctor/doctor_view.html', context)
@login_required
def prescription(request , pid):
    username = request.user.username
    docname =Doctor.objects.filter(dname=username).distinct()
   
    new = Patient_Details.objects.filter(doctor=username,id=pid)
   
    items = History.objects.filter(p_id_id=pid).order_by('-date')[:1] 


    context={
        'new':new,
        'docname':docname,
        'items':items,
    }
    
    return render(request, 'doctor/prescription.html',context)


def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Patient_Details.objects.filter(name__icontains=q)
        #multiple_q = Q(Q(name__icontains=q) | Q(place__icontains=q))
        #data = Patient.objects.filter(multiple_q)
    else:
        data = Patient_Details.objects.all()
    context = {
        'data': data
    }
    return render(request, 'doctor/doctor_view_appointment.html', context)


def doctor_add_prescription(request, pid):
    if request.method == "POST":
        symptoms = request.POST.get('symp')
        tests = request.POST.get('tests')
        advice = request.POST.get('advice')
        medicine = request.POST.get('medicine')
        patient = Patient_Details.objects.get(id=pid)
        item = History(symptoms=symptoms, tests=tests, advice=advice, medicine=medicine, p_id=patient)
        item.save()
        messages.info(request, "ITEM ADDED SUCCESSFULLY")
    items = History.objects.all()
    new = Patient_Details.objects.get(id=pid)
    item = Patient_Details.objects.all()
    context = {
        'items': items,
        'item': item,
        'new': new
    }
    return render(request, 'doctor/doctor_add_prescription.html',context)

# import datetime
# def create_appointment(request):
#     if request.method == 'POST':
#         doctor_id = request.POST['doctor_id']
#         patient_id = request.POST['patient_id']
#         appointment_date = request.POST['appointment_date']
#         appointment_time = request.POST['appointment_time']

#         doctor = Doctor.objects.get(id=doctor_id)
#         patient = Patient_Details.objects.get(id=patient_id)

#         # Validate appointment date and time
#         appointment_datetime = datetime.datetime.combine(appointment_date, appointment_time)
#         day_of_week = appointment_date.strftime("%A")

#         try:
#             doctor_schedule = DoctorSchedule.objects.get(doctor=doctor, day=day_of_week)
#             if doctor_schedule.start_time <= appointment_time <= doctor_schedule.end_time:
#                 # Appointment time is within doctor's schedule
#                 appointment = Appointment(doctor=doctor, patient=patient, appointment_datetime=appointment_datetime)
#                 appointment.save()
#                 # Redirect or render success message
#                 messages.success(request, "Appointment created successfully!")
#             else:
#                 # Appointment time is not within doctor's schedule
#                 # Render error message
#                 messages.error(request, "Selected appointment time is not available for the doctor.")
#         except DoctorSchedule.DoesNotExist:
#             # Doctor does not have a schedule for the selected day
#             # Render error message
#             messages.error(request, "Doctor does not have a schedule for the selected day.")

#     # Provide necessary context data for rendering the form template
#     doctors = Doctor.objects.all()
#     patients = Patient_Details.objects.all()
#     context = {
#         'doctors': doctors,
#         'patients': patients
#     }

#     return render(request, 'create_appointment.html', context)


