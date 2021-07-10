from django import forms
from loginPassword.validators import file_size_profile_photo
from django.core.validators import FileExtensionValidator
from patient.models import PatientRegister




class PRegistrationForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type Patient Full Name'}),label='Patient Name',max_length=50,min_length=4,required=True)
    dob=forms.CharField(label="DOB",widget=forms.TextInput(attrs={'type': 'date','placeholder': 'DD/MM/YYYY'}),required=False)    
    gender=forms.ChoiceField(label="Gender",choices= (('male', "Male"),('female', "Female"),('other', "Other")),required=True)
    mobile=forms.CharField(label="Patient Mobile",max_length=12,min_length=10,required=True)
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Type Patient Email'}),label='Email',max_length=50,min_length=6,required=False)
    address=forms.CharField(widget=forms.TextInput(attrs={'title': "Enter Patient postal address",'placeholder': "Address"}),label="Address",max_length=200,min_length=4,required=False) 
    photo=forms.ImageField(allow_empty_file=True,label="Patient photo",help_text='accept JPG/PNG file,max size 60 kb',required=False,validators=[file_size_profile_photo,FileExtensionValidator(allowed_extensions=['jpg','png'])])
    class Meta:
        model = PatientRegister
        fields = ('name','dob','gender','mobile','email','address','photo')