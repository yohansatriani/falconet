from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from falconet.forms import LoginForm

@login_required()
def home(request):
    html = render_to_string('page-home.html', {'title': "Home", 'head': "Home"})
    return HttpResponse(html)

def auth_login(request):
    if not request.user.is_authenticated:
        form = LoginForm()
        return render(request, 'page-login.html', {'title': "Login", 'head': "Login", 'form': form})
    else:
        return redirect(home)

def auth_logout(request):
    logout(request)
    return redirect(auth_login)

def auth_process(request):
    if request.method == 'POST':    
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            return redirect(auth_login)
    else:
        if not request.user.is_authenticated:
            return redirect(auth_login)
        else:
            return redirect(home)

