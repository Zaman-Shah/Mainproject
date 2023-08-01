from django.contrib import admin
from . models import History,DoctorSchedule,Appointment
#
# Register your models here.
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('p_id', 'symptoms', 'tests', 'advice', 'medicine', 'date')

admin.site.register(History, HistoryAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'appointment_date')

admin.site.register(Appointment, AppointmentAdmin)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'start_time', 'end_time','on_leave')

admin.site.register(DoctorSchedule, ScheduleAdmin)