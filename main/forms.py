from django import forms

class SuperuserCreationForm(forms.Form):
    secret_key = forms.CharField(widget=forms.PasswordInput, label="Secret Key")
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")