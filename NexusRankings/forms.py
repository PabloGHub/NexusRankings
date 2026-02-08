from django import forms
from django.contrib.auth.forms import AuthenticationForm

from NexusRankings.models import Usuario, Reputacion

class RegistrarForm(forms.ModelForm):
    contra:str = forms.CharField(label='Contraseña', max_length=100, widget = forms.PasswordInput)
    contra2:str = forms.CharField(label='Repite Contraseña', max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('nombre', 'contra')

class LoguearForm(AuthenticationForm): # AuthenticationForm
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    # contra = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('nombre', 'contra')


class ReputacionForm(forms.Form):
    score:int = forms.IntegerField(label="Puntuacion", min_value=0, max_value=5,
                                   widget=forms.NumberInput(attrs={'type': 'range', 'class': 'rango'}))
    summary:str = forms.CharField(label='Resumen', max_length=400, widget=forms.Textarea(attrs={'class': 'campo-texto'}))
    # texto:str = forms.CharField(label='Texto', max_length=400)

    class Meta:
        model = Reputacion
        fields = ('score', 'summary')