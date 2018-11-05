from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from falconet.forms import LoginForm
from netinfo.models import sites as sites_model, contacts as contacts_model

@login_required()
def home(request):
    html = render_to_string('page-home.html', {'title': "Home", 'head': "Home", 'bcitems': [['home', 'Home']]})
    return HttpResponse(html)

@login_required()
def sites(request):
    sites_data = sites_model.objects.all()
    html = render_to_string('page-sites.html', {'title': "Sites", 'head': "Sites", 'bcitems': [['home', 'Home'], ['sites', 'Sites']], 'sites_data': sites_data })
    return HttpResponse(html)

@login_required()
def site_office(request):
    sites_data = sites_model.objects.filter(type__in = ['HO', 'KC', 'KCP', 'KK'])
    html = render_to_string('page-sites.html', {'title': "Sites", 'head': "Sites", 'bcitems': [['home', 'Home'], ['sites', 'Sites'], ['office', 'Office']], 'sites_data': sites_data })
    return HttpResponse(html)

@login_required()
def site_isp(request):
    sites_data = sites_model.objects.filter(type__in = ['ISP', 'POP'])
    html = render_to_string('page-sites.html', {'title': "Sites", 'head': "Sites", 'bcitems': [['home', 'Home'], ['sites', 'Sites'], ['isp', 'ISP']], 'sites_data': sites_data })
    return HttpResponse(html)

@login_required()
def site_detail(request, site_id):
    try:
        site_id = int(site_id)
    except ValueError:
        raise Http404()
    sites_data = get_object_or_404(sites_model, id=site_id) 
    contacts_data = contacts_model.objects.filter(site = site_id)
    html = render_to_string('page-site-detail.html', {'title': "Sites", 'head': "Sites", 'bcitems': [['home', 'Home'], ['sites', 'Sites'], [site_id, sites_data.name]], 'sites_data': sites_data ,'contacts_data': contacts_data})
    return HttpResponse(html)

@login_required()
def site_detail_edit(request, site_id):
    try:
        site_id = int(site_id)
    except ValueError:
        raise Http404()
    sites_data = get_object_or_404(sites_model, id=site_id)
    contacts_type = contacts_model.objects.values('type').distinct()
    contacts_data = contacts_model.objects.filter(site = site_id)
    html = render_to_string('page-site-detail-edit.html', {'title': "Sites", 'head': "Sites", 'bcitems': [['home', 'Home'], ['sites', 'Sites'], [site_id, sites_data.name]], 'sites_data': sites_data ,'contacts_data': contacts_data, 'contacts_type': contacts_type})
    return HttpResponse(html)

# AJAX
def get_contacts_type(request):
    # contacts_type = contacts_model.objects.filter(site = 0)
    # contacts_type_xml = serializers.serialize("xml", contacts_type, fields=('type'))
    contacts_type = {'contacts_type': ['phone','fax']}
    # contacts_type = [{ "type" : "phone"},{ "type" : "fax"}]
    return JsonResponse(contacts_type)

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

