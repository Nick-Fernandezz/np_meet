from django.forms import ModelForm
from django import forms
from .models import Corporations, CompInvites


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

