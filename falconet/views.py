from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from falconet.forms import LoginForm

from netinfo.forms import SiteForm
from netinfo.models import sites as sites_model, contacts as contacts_model
from netinfo.views import sites, site_isp, site_office, site_detail, site_detail_edit, site_edit_process

# Create your views here.
@login_required()
def home(request):
    html = render_to_string('page-home.html', {'title': "Home", 'head': "Home", 'bcitems': [['home', 'Home']]})
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

# AJAX
def get_contacts_type(request):
    # contacts_type = contacts_model.objects.filter(site = 0)
    # contacts_type_xml = serializers.serialize("xml", contacts_type, fields=('type'))
    contacts_type = {'contacts_type': ['phone','fax']}
    # contacts_type = [{ "type" : "phone"},{ "type" : "fax"}]
    return JsonResponse(contacts_type)


