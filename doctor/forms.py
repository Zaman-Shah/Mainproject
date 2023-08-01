from django import forms
from django.utils import timezone
class MyForm(forms.Form):
    my_date_field = forms.DateField(widget=forms.DateInput(attrs={'max': timezone.now().strftime('%Y-%m-%d')}))
