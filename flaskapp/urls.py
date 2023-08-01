from django.urls import path,include
import urllib3
from . views import add_item,delete,chatbot,admin_update_patient,admin_home_view,departments,admin_view_patients,admin_view_appointments,admin_add_appointments,admin_view_doctors,admin_view_department
from . import views
from .views import *
#admin_view_history,
urlpatterns = [
   
    path('chatbot',chatbot,name='chatbot'),
    path('admin_home_view',admin_home_view,name='admin_home_view'),
    path('departments',departments,name='departments'),
    path(r'^$',admin_view_patients,name='admin_view_patients'),
  
    path('admin_view_appointments',admin_view_appointments,name='admin_view_appointments'),
    path('admin_add_appointments',admin_add_appointments,name='admin_add_appointments'),
    #path('admin_view_history',admin_view_history,name='admin_view_history'),  
    #path('admin_edit_patient/',admin_edit_patient,name='admin_edit_patient'),
   
    path('admin_view_doctors',admin_view_doctors,name='admin_view_doctors'),
    path('admin_view_department',admin_view_department,name='admin_view_department'),
    path(r'^delete/(?P<pid>\d+)/$', delete, name='delete'),
   
   
    path('admin_update_patient/<int:pid>',admin_update_patient,name='admin_update_patient'),
   
    path('edit_item/<int:pid>/',edit_item,name="edit_item"),
    path('add_item',add_item,name='add_item'),
    path('add_dept',add_dept,name='add_dept'),
    path('view_schedule/<int:did>/',view_schedule,name='view_schedule'),
    path('schedule/',schedule,name='schedule'),
    path('edit_doctor_item/<int:pid>/',edit_doctor_item,name='edit_doctor_item'),
    path('admin_update_doctor/<int:pid>',admin_update_doctor,name='admin_update_doctor')
    
    
] 