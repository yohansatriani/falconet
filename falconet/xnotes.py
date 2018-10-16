from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from falconet import forms
from falconet.views import login, home, auth_process, auth_login

path('login/', auth_views.login, {
    'template_name': 'page-login.html',
    'authentication_form': forms.LoginForm,
    'extra_context': {
            'title': 'Login',
            'head': 'Login',
        },
    },
),