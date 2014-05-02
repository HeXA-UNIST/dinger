import datetime
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    user = forms.CharField(max_length=100)
    passwd = forms.CharField(max_length=100, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    passwd = forms.CharField(max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField()

    name = forms.CharField(max_length=32)
    birthday = forms.DateField(initial=datetime.date.today)
    intro = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=11)

    def is_registered(self):
    	try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
        	return False
       	return True
            


