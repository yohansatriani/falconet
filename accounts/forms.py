from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete':'off','class': 'form-control', 'id': 'username'}))

    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={'autocomplete': 'off','class': 'form-control', 'id': 'password'})) 