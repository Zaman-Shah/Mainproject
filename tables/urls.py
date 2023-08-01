from django.urls import path

from .views import patient_details,add_minutes

urlpatterns = [
    #1path('', hello),
    #path('chatbot', chatbot),
    #path('whatsapp_webhook', whatsapp_webhook, name='whatsapp_webhook'),
    path('patient_details',patient_details,name='patient_details'),
    #path('patient_data_eg',patient_data_eg,name='patient_data_eg'),
    #path('bot_wtsp',bot_wtsp,name='bot_wtsp'),
    path('add_minutes',add_minutes,name='add_minutes')
]
