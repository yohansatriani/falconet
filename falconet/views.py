from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from falconet.forms import LoginForm

@login_required()
def home(request):
    html = render_to_string('page-home.html', {'title': "Home", 'head': "Home", 'bcitems': ['home']})
    return HttpResponse(html)

@login_required()
def sites(request):
    html = render_to_string('page-sites.html', {'title': "Sites", 'head': "Sites", 'bcitems': ['home', 'sites']})
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
        next_url = request.POST['next']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            else:
                return redirect(home)
        else:
            messages.error(request,'Authentication Failed: Username or password is incorrect')
            return redirect(auth_login)
    else:
        if not request.user.is_authenticated:
            return redirect(auth_login)
        else:
            return redirect(home)

