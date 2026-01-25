from django import forms
from django.contrib.auth.forms import AuthenticationForm

from NexusRankings.models import Usuario

class RegistrarForm(forms.ModelForm):
    contra:str = forms.CharField(label='Contraseña', max_length=100, widget = forms.PasswordInput)
    contra2:str = forms.CharField(label='Repite Contraseña', max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('nombre', 'contra')

class LoguearForm(AuthenticationForm):
    nombre = forms.CharField(label='Nombre de usuario', max_length=100)
    contra = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)