from django import forms

from .models import  DeliveryLocation



class DeliveryLocationForm(forms.ModelForm):
    class Meta:
        model = DeliveryLocation
        exclude = ['id']