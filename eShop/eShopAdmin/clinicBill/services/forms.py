from django import forms
from services.models import Service





class ServiceForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Service Name'}),label='Service Name',max_length=50,min_length=2,required=True)
    price=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Service Cost'}),label='Service Price',max_length=15,min_length=2,required=True)
    class Meta:
        model = Service
        fields = ('name','price')