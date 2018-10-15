from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

# from accounts.forms import LoginForm
from falconet import forms

def login(request):
    html = render_to_string('page-login.html', {'title': "Login", 'head': "Login"})
    return HttpResponse(html)

def home(request):
    html = render_to_string('page-home.html', {'title': "Home", 'head': "Home"})
    return HttpResponse(html)

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect(home)
    else:
        return redirect('../login/')