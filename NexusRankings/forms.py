from django import forms

class loguear(forms.Form):
    nombre:str = forms.CharField(max_length=100, label='Nombre de usuario')
    contra:str = forms.CharField(max_length=100, label='Contraseña', widget=forms.PasswordInput)
