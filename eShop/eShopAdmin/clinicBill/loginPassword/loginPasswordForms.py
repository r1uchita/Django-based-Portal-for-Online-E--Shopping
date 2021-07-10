from django import forms




class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type Your Username'}),label='Username',max_length=15,min_length=4,required=True)
    passwd=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Type Your Password'}),label='Password',max_length=15,min_length=3,required=True)


