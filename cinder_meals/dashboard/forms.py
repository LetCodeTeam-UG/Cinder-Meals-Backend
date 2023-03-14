from django import forms

from .models import  DeliveryLocation, Meal



class DeliveryLocationForm(forms.ModelForm):
    class Meta:
        model = DeliveryLocation
        exclude = ['id']

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = [ 'image','title', 'description', 'price', 'published']