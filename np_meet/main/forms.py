from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Corporations, CompInvites, User


class CreateCompanyForm(ModelForm):

    class Meta:
        model = Corporations
        fields = ['name', 'logo']


class CreateWorckerInviteForm(ModelForm):

    class Meta:
        model = CompInvites
        fields = ['max_activations']


class JoinWorkerInviteForm(forms.Form):
    
    code = forms.CharField(max_length=100, label='Код приглашения', strip=True)


class SingUPForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")



class EditUserForm(ModelForm):

    class Meta:
        model = User
        fields = ('avatar', 
                  'username', 
                  'first_name', 
                  'last_name', 
                  'birth_date',
                  'phone')
        
