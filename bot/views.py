from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import sqlite3
from accounts.models import Patient_Details
#, Patient
from django.db import connection, transaction


@csrf_exempt
@twilio_view
def chat_bot(request):
    if request.method == 'POST':
        incoming_msg = request.POST.get('Body', '').lower()
        receiver_phone_no = request.POST.get('From', '')
        response = MessagingResponse()
        resp = response.message()
        respons = ""

        # 123message = Patient(from_number=from_number, to_number=to_number, body=body)
        # 1message.save()

    if 'hai' in incoming_msg or 'hello' in incoming_msg or "booking" in incoming_msg or "hi" in incoming_msg or "morning" in incoming_msg or "hlo" in incoming_msg:
        respons = "Good Morning...." \
                  "Welcome to MedCare....." \
                  "Please enter your name"
        conn = sqlite3.connect('chatbot.db')
        print('database connected successfully')
        cur = conn.cursor()

        conn.close()

        account_sid = 'ACb828895438c99ae4a1a89cbc8faa2096'
        auth_token = 'f95011ad947de9a307b719a17c7cf87f'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=respons,
            from_='whatsapp:+14155238886',
            to=receiver_phone_no
        )

        print(message.sid)
        print(incoming_msg)
        print(receiver_phone_no)

        return HttpResponse(str(resp))
    # if (mainInput == 1):
        # if(todayCount<10):
        # if (subInput == 0):

    # if 'hi' in incoming_msg:
        # pname=incoming_msg
        # print(pname)

    # elif 'good morning' in incoming_msg:
        #respons = "Good morning... Have a nice day..."
    # else:
       # respons = "Sorry... I didn't get you"


@csrf_exempt
@twilio_view
def whatsapp_webhook(request):
    if request.method == 'POST':
        from_number = request.POST.get('From')
        to_number = request.POST.get('To')
        body = request.POST.get('Body')
        response = MessagingResponse()
        resp = response.message()

        responded = False
        print(resp)
        print(body)
        respons = ""
        if body:
            if 'hi' in body:
                respons = "Hello...How can I help you?"
                resp.body(respons)
                responded = True
            if 'booking' or 'book' or 'appointment' or 'consult' in body:
                respons = "Please select a department:"\
                    "1.Pediatrition"\
                    "2.General medicine"\
                    "3.Oncology"\
                    "4.Dermatology"
                resp.body(respons)
                if '1.pediatrition' in body:
                    respons = "Please select Doctor in pediatrics"\
                        "1.Dr.Samual"\
                        "2.Dr.Bcd"
                    resp.body(respons)
                # 2msg = WhatsAppMessage(from_number=from_number, to_number=to_number, body=body )
                # msg.save()
                    dept = body
                # print(dept)
                # 2data = Patient(department=body)
                # data.save()
                    if '1.Dr.Samual' in body:
                        respons = "Please enter your name"
                    # 2data = Patient(doctor=body)
                    # data.save()
                        # 2data = Patient(name=body)
                        # data.save()
                    elif 'Bcd' in body:
                        respons = "Please enter your name"
                        # print(doctor)
                    else:
                        respons = "please enter correct doctor name"

                elif '2.General Medicine' in body:
                    respons = "Please select Doctor in pediatrics"\
                        "1.Dr.A"\
                        "2.Dr.B"
                    data = Patient_Details(department=body)
                    data.save()
                elif '3.Oncology' in body:
                    respons = "Please select Doctor in pediatrics"\
                        "1.Dr.Ab"\
                        "2.Dr.Bc"
                #data = Patient(department=body)
                # data.save()
                    if '1.Dr.Ab' in body:
                        respons = "Please enter your name"
                elif '4.Dermatology' in body:
                    respons = "Please select Doctor in pediatrics"\
                        "1.Dr.Abd"\
                        "2.Dr.Bdc"
                    data = Patient_Details(department=body)
                    data.save()

                # 2sql = "INSERT INTO  WhatsAppMessage(from_number, to_number, body) VALUES (%s, %s, %s)"
                #values = (from_number, to_number, body)

        # Execute the query
                # with connection.cursor() as cursor:
                    #cursor.execute(sql, values)

        account_sid = 'ACb828895438c99ae4a1a89cbc8faa2096'
        auth_token = 'f95011ad947de9a307b719a17c7cf87f'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=respons, from_=to_number, to=from_number)

        # 1msg = WhatsAppMessage(from_number=from_number, to_number=to_number, body=body )
        # msg.save()

    return HttpResponse(str(resp))


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
    'doctor_input':0,}
}


@csrf_exempt
@twilio_view
def patient_data(request):
    # global globelvar.subinput
    # global globelvar.userdatas
    # global maininput
    # global dept_input
    # global doctor_input
    global todayCount
    global globelvar
    pname=""
    age = 0
    department = ""
    doctor=""
    place = ""
    new_id=0
    
    if request.method == 'POST':
        from_number = request.POST.get('From')
        to_number = request.POST.get('To')
        body = request.POST.get('Body').lower()
        response = MessagingResponse()
        resp = response.message()
        respons = "null"
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
                }
            todayCount = Patient_Details.objects.count()
            print(todayCount)
            globelvar[from_number]['maininput'] = 1
            
    

        if globelvar[from_number]['maininput'] == 1:
            if todayCount < 200:
                if 'booking'in body  or 'book'in body  or 'appointment' in body or 'consult' in body:
                    respons = "Please select a department:..........."\
                        "1.Pediatrician..........."\
                        "2.General medicine.........."\
                        "3.Oncology..........."\
                        "4.Dermatology.............."
                    globelvar[from_number]['dept_input'] = 0
                if globelvar[from_number]['dept_input'] == 0:
                    if 'pediatrician' in body:
                        department = body
                        globelvar[from_number]['userdatas']['department'] = department
                        respons = "Please select Doctor in pediatrics......"\
                            "1.Dr.Samual....."\
                            "2.Dr.Bcd........"
                        #my_model = Patient(department=department)
                        #my_model.save(new_id)
                        responded = True
                    elif 'general' in body:
                        department = body
                        globelvar[from_number]['userdatas']['department'] = department
                        respons = "Please select Doctor in General medicine......"\
                            "1.Dr.Raheem....."\
                            "2.Dr.Zaman........"
                        responded = True
                    if globelvar[from_number]['subinput'] == 1:
                        pname = body
                        print(pname)
                        globelvar[from_number]['userdatas']['name'] = pname
                        respons = "Thanks for entering your name.....Please enter your age"
                        #my_model = Patient(name=pname)
                        #my_model.save(new_id)
                        globelvar[from_number]['subinput'] = globelvar[from_number]['subinput']+1
                    elif globelvar[from_number]['subinput'] == 2:
                        age = body
                        print(age)
                        globelvar[from_number]['userdatas']['age'] = age
                        respons = "Thanks for entering your age.....Please enter your place"
                        #my_model = Patient(age=age)
                        #my_model.save(new_id)
                        globelvar[from_number]['subinput'] = globelvar[from_number]['subinput']+1
                    elif globelvar[from_number]['subinput'] == 3:
                        place = body
                        globelvar[from_number]['userdatas']['place'] = place
                        
                        respons = "Thanks for entering your place....which date you want to book? "
                        #my_model = Patient(place=place)
                        #my_model.save(new_id)
                        dict_data = Patient_Details(**globelvar[from_number]['userdatas'])
                        dict_data.save()
                        
                        globelvar[from_number]['subinput'] = globelvar[from_number]['subinput']+1
                        
                        
                    # elif globelvar[from_number]['subinput'] == 4:
                    #     date = body
                    #     globelvar[from_number]['userdatas']['date'] = date
                    #     print(userdatas)
                    #     respons = "Thanks for choosing date.....which time u want ?"
                    #     #my_model = Patient(place=place)
                    #     #my_model.save(new_id)
                    #     #dict_data = Patient(**globelvar[from_number]['userdatas'])
                    #     #dict_data.save()
                        
                        
                    #     globelvar[from_number]['subinput'] = globelvar[from_number]['subinput']+1
                        
                    # elif globelvar[from_number]['subinput'] == 4:
                    #     time = body
                    #     globelvar[from_number]['userdatas']['app_date_time'] = time
                        
                    #     respons = "Thanks for choosing time.....Booking completed"
                    #     #my_model = Patient(place=place)
                    #     #my_model.save(new_id)
                    #     dict_data = Patient_Details(**globelvar[from_number]['userdatas'])
                    #     dict_data.save()
                        
                    #     globelvar[from_number]['subinput'] = globelvar[from_number]['subinput']+1
                        
                        
                        
                    if 'samual' in body:
                        print('inDoctor------------------------------------')
                        doctor = body
                        print(doctor)
                        globelvar[from_number]['userdatas']['doctor'] = doctor
                        respons = "please enter your name"
                        #my_model = Patient(doctor=doctor)
                        #my_model.save(new_id)
                        globelvar[from_number]['subinput'] = globelvar[from_number]['subinput']+1
                    

                    
                        globelvar[from_number]['doctor_input'] = 0

            

            #id_list = Patient.objects.values_list('id', flat=True)
            #print(id_list)
            #last_object = Patient.objects.latest('id')
            #print(last_object)
            #last = Patient.objects.last()
            #new_id=last.id+1
            #print(new_id)
            #userdatas={'id':new_id}

        if globelvar[from_number]['subinput'] == 4:
            globelvar[from_number]['maininput'] = 0
            globelvar[from_number]['subinput'] = 0
            globelvar[from_number]['dept_input'] = 0
            globelvar[from_number]['doctor_input'] = 0

        print(respons)
        print(userdatas)
        
        
        account_sid = 'ACb828895438c99ae4a1a89cbc8faa2096'
        auth_token = 'f95011ad947de9a307b719a17c7cf87f'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=respons, from_=to_number, to=from_number)
    return HttpResponse(str(resp))


@csrf_exempt
@twilio_view
def patient_data_eg(request):
    global msg
    global from_number
    global to_number
    if request.method == 'POST':
        from_number = request.POST.get('From')
        to_number = request.POST.get('To')
        body = request.POST.get('Body').lower()
        msg = str(body)
        # print(body)
        response = MessagingResponse()
        resp = response.message()
        bot_wtsp(msg, resp)

    return HttpResponse(str(msg, resp))


@csrf_exempt
@twilio_view
def bot_wtsp(msg, resp):
    global subinput
    global userdatas
    global maininput
    global dept_input
    global doctor_input

    print("message"+msg)
    response = MessagingResponse()
    resp = response.message()
    respons = ""

    if maininput == 1:
        if 'booking' or 'book' or 'appointment' or 'consult' in msg:
            respons = "Please select a department:..........."\
                "1.Pediatrician..........."\
                "2.General medicine.........."\
                "3.Oncology..........."\
                "4.Dermatology.............."
            dept_input = 0
            if dept_input == 0:
                if 'pediatrician' in msg:
                    department = msg
                    userdatas['department'] = department
                    respons = "Please select Doctor in pediatrics......"\
                        "1.Dr.Samual....."\
                        "2.Dr.Bcd........"

                    if 'Samual' in msg:
                        doctor = msg
                        print(doctor)
                        userdatas['doctor'] = doctor
                        respons = "please enter your name"

                        if subinput == 0:
                            patiet_name = msg
                            userdatas['name'] = patiet_name
                            respons = "Thanks for entering your name.....Please enter your age"
                            subinput = subinput+1
                        elif subinput == 1:
                            age = msg
                            userdatas['age'] = age
                            respons = "Thanks for entering your age.....Please enter your place"
                            subinput = subinput+1
                        elif subinput == 2:
                            place = msg
                            userdatas['place'] = place
                            respons = "Thanks for entering your place.....Booking completed"
                            subinput = subinput+1
                        else:
                            respons = "Todays booking completed. Try tommorow"

                elif 'general' in msg:
                    department = msg
                    userdatas['department'] = department
                    respons = "Please select Doctor in General medicine......"\
                        "1.Dr.Raheem....."\
                        "2.Dr.Zaman........"
                    doctor_input = 0
    if 'hai' in msg or 'hello' in msg or "booking" in msg or "hi" in msg or "morning" in msg or "hlo" in msg:
        respons = "Good Morning...." \
            "Welcome to MedCare....." \
            "How can i help you..."
        todayCount = Patient_Details.objects.count()
        print(todayCount)
        maininput = 1
    if subinput == 3:
        maininput = 0
        subinput = 0
        dept_input = 0
        doctor_input = 0

    account_sid = 'ACb828895438c99ae4a1a89cbc8faa2096'
    auth_token = 'f95011ad947de9a307b719a17c7cf87f'
    client = Client(account_sid, auth_token)
    # session = client.proxy.v1 \.services('KSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \.sessions \.create()
    #service = client.proxy.v1.services.create(unique_name='unique_name')
    message = client.messages.create(
        body=respons, from_=to_number, to=from_number)
    return HttpResponse(str(resp))


