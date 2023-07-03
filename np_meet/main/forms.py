from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


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
        

class CreateTaskForm(ModelForm):

    class Meta:
        model = Tasks
        fields = (
            'task',
            'worker',
            'deadline',
        )
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
       if 'company' in kwargs and kwargs['company'] is not None:
           company = kwargs.pop('company')
           qs = User.objects.filter(corporation=company)

       # вызываем конструктор формы и добавляет query set
       super(CreateTaskForm, self).__init__(*args, **kwargs)
       try:
           self.fields['worker'].queryset = qs
       except NameError:
           pass


