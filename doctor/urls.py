from django.urls import path
from .views import doctor_home_view,prescription,doctor_view_appointment,doctor_view_patient,doctor_view_history,search,doctor_add_prescription



urlpatterns = [
    path('doctor_home/',doctor_home_view,name='doctor_home_view'),
    path('prescription/<int:pid>',prescription,name='prescription'),
    path('doctor_view_appointment',doctor_view_appointment,name='doctor_view_appointment'),
    path('doctor_view_patient',doctor_view_patient,name='doctor_view_patient'),
    path('doctor_view_history/<int:pid>',doctor_view_history,name='doctor_view_history'),
    path("search", search, name='search'),
    path('doctor_add_prescription/<int:pid>',doctor_add_prescription,name='doctor_add_prescription')
]