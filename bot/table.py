import sqlite3
from flask import Flask,render_template,request,session, redirect, jsonify
from django.shortcuts import render,redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import request , Flask
from datetime import datetime,timedelta

app = Flask(__name__)

mainInput =0
subInput =0
patiet_name = ""
todayCount=0
madedSession={}
userdatas={}


@app.route('/chatbot',methods=["POST"])
def chatbot():
    global mainInput
    global  patiet_name
    global subInput
    global todayCount
    global userdatas
    global madedSession
    
    incoming_msg = request.values.get('Body', '').lower()
    recieverPhoneNo = request.values.get('From', '')
    response = MessagingResponse()
    resp = response.message()
    respons=""
    if (mainInput == 1):
        if todayCount < 10:
            if subInput == 0:
                patiet_name = incoming_msg
                userdatas['name']=patiet_name
                todaydate = now.strftime("%d-%m-%Y")
                conn = sqlite3.connect('chatbot.db')
                cur = conn.cursor()
                query = cur.execute("SELECT pname,date from patient where phone = '%s' AND pname = '%s'" %(recieverPhoneNo,patiet_name))
                print(query)
                arrayData = cur.fetchall()
                conn.commit()
                conn.close()
                print(arrayData)
                if(len(arrayData)>0 and todaydate==date):
                    respons='This patient has already booked'
                    subInput =3
                else:
                    respons = "Thanks for entering your name...\nPlease enter your place"
                    subInput = subInput + 1
        
    
    if 'hai' in incoming_msg or 'hello'in incoming_msg or "booking" in incoming_msg or "hi" in incoming_msg or "morning" in incoming_msg or "hlo" in incoming_msg:
        respons = "Good Morning...." \
                  "Welcome to MedCare....." \
                  "Please enter your name"
        conn = sqlite3.connect('chatbot.db')
        cur = conn.cursor()
        qry = cur.execute("SELECT count(*) FROM `patient` WHERE `date`='%s'" % date)
        todayCount =qry.fetchall()[0]['count(*)']
        conn.commit()
        conn.close()
        print(todayCount)
    elif 'cancel' in incoming_msg:
        respons = "It will automatically cancelled if you don't admit...!"
    elif mainInput ==0:
        respons = "i did not get you"

    if(subInput==3):
        mainInput=0
        subInput=0
    
    
    account_sid = 'ACe1bfccfb63fcdd2f225104a43c83d77b'
    auth_token = '3a100c9258ff05d5fc65d7cd98139acd'
    client= Client(account_sid, auth_token)
    
    
    
    message = client.messages.create(body=respons,
            from_='whatsapp:+14155238886',
            to=recieverPhoneNo
            )

    print(message.sid)
    print(incoming_msg)
    print(recieverPhoneNo)
  
    
    return str(resp)

