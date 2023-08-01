from django import forms

class MyForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
    place = forms.CharField()
    department = forms.CharField()
    doctor =forms.CharField()
    height = forms.FloatField()
    weight = forms.FloatField()