from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login as auth_login
import soupsieve
import flaskapp
from flaskapp.views import admin_home_view
from . models import Doctor
from bot.models import department_list
from django.views.generic import ListView,DetailView
import bs4
from .models import Patient_Details
from django.db.models import Q
from django.contrib.auth import get_user_model

# Create your views here.
def home(request):
    return render(request,'home.html')


def register(request):
    options = department_list.objects.all()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email =request.POST['email']
        department =request.POST['department']
        qualification =request.POST['qualification']
        experience =request.POST['experience']
        phone =request.POST['contact']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        data = Doctor(dname=username, department=department, qualification=qualification, experience=experience, contact=phone, email=email)
        data.save()
        #options = department_list.objects.all()  # Retrieve data from your table
        #print(options)
        #context = {
        #'options': options,
        #}
        #print(context)
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email is exist ')
                return redirect(register) 
            else:
                user = User.objects.create_user(username=username,password=password, email=email, first_name=first_name, last_name=last_name )
                user.set_password(password) 
                user.save()
                print("success")
                return redirect('login_user') 
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        print("no post method")
        context = {
        'options': options,
        }
        return render(request, 'register.html',context) 
    
    
def login_user(request):
    if request.method == 'POST':
        username =request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        # admin = get_user_model()
        # superusers = admin.objects.filter(is_superuser=True)
        # print(superusers)
        if user is not None :
            auth.login(request, user)
            if user.is_superuser:
                return redirect('adminhome')
            else:
                return redirect('doctor_home')
            # if user.is_superuser:  # Check if the user is a superuser
            #     auth.login(request, user)
            #     return redirect('adminhome')
            # else:
            #     auth.login(request, user)
            #     return redirect('doctor_home')
            # auth.login(request, user)
            # return redirect('doctor_home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')
    else:
        return render(request, 'login.html')
    
    
def logout_user(request):
    auth.logout(request)
    return redirect('home') 






# class SearchViewDetail(DetailView):
    
#     model = Patient
#     template_name='admin_doctor.html'
#     context_object_name="post"
    
#     def get_queryset(self):
#         queryset = self.request.GET.get('q')
#         return Patient.objects.filter(name__contains=queryset)
    

# def search_venues(request):
#     if request.method == "POST":
#         searched =request.POST['searched']
#         #soup = bs4.BeautifulSoup(html)
#         #tables = soupsieve.find_all('table')
#         patient = Patient.objects.filter(name__contains=searched)
#         # for table in tables:
#         #     # Get the rows from the table
#         #     rows = table.find_all('tr')
#         #     # Filter the rows by the search term
#         #     filtered_rows = [row for row in rows if searched in row.text]
#         #     # If there are filtered rows, then return them
#         #     if filtered_rows:
#         return render(request, 'admin_doctor.html',{'searched':searched},{'Patient':patient})
#     else:
#         return render(request, 'admin_doctor.html',{})
    
    
def index(request):
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
    return render(request, 'admin_temp/pages/examples/admin_view_appointment.html', context)


# def index(request):
#     query = request.GET.get('q')
#     if query:
#         results = Patient_Details.objects.filter(Q(id__icontains=query)).distinct()
#         context = {'results': results}
#         return render(request, 'admin_temp/pages/examples/admin_view_appointment.html', context)
#     else:
#         return render(request, 'admin_temp/pages/examples/admin_view_appointment.html')