from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class LoginUSer(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=60, widget=forms.PasswordInput, required=True)

class CreateUser(forms.ModelForm):

    password1 = forms.CharField(max_length=60, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=60, required=True, widget=forms.PasswordInput, label='Repeat Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def cleaned_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
                raise forms.ValidationError('Both Password Dont Match')
        return cd['password2']

class CreateNewUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'date_of_birth']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']