from django.urls import path

from .views import whatsapp_webhook,patient_data,patient_data_eg,bot_wtsp

urlpatterns = [
    #1path('', hello),
    #path('chatbot', chatbot),
    path('whatsapp_webhook', whatsapp_webhook, name='whatsapp_webhook'),
    path('patient_data',patient_data,name='patient_data'),
    path('patient_data_eg',patient_data_eg,name='patient_data_eg'),
    path('bot_wtsp',bot_wtsp,name='bot_wtsp'),
]
