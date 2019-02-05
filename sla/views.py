from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from falconet import views
from falconet.forms import LoginForm

# from netinfo.forms import SiteForm, ContactForm, LinkForm, DevForm
# from netinfo.models import sites as sites_model, contacts as contacts_model, links as links_model, devices as dev_model

from sla.forms import TroubleForm

from pprint import pprint
# Create your views here.

@login_required()
def trouble_post(request):
    if request.method == 'POST':
        pprint(request.POST)
    #     dev_post_data = {
    #         'id':1000,
    #         'type':request.POST['type'],
    #         'model':request.POST['model'],
    #         'name':request.POST['name'],
    #         'ipadd':request.POST['ipadd'],
    #         'location':request.POST['location'],
    #         'status':request.POST['status'],
    #         'serial_number':request.POST['serial_number'],
    #         'os':request.POST['os'],
    #         'tagline':request.POST['tagline'],
    #         'input_date':request.POST['input_date'],
    #     }
    #     pprint("Post Trouble")
    #
    #     dev_form = DevForm(dev_post_data)
    #
    #     if dev_form.is_valid():
    #         type = dev_form.cleaned_data['type']
    #         model = dev_form.cleaned_data['model']
    #         name = dev_form.cleaned_data['name']
    #         ipadd = dev_form.cleaned_data['ipadd']
    #         location =dev_form.cleaned_data['location']
    #         status = dev_form.cleaned_data['status']
    #         serial_number = dev_form.cleaned_data['serial_number']
    #         os = dev_form.cleaned_data['os']
    #         tagline = dev_form.cleaned_data['tagline']
    #         input_date = dev_form.cleaned_data['input_date']
    #
    #         dev_add = dev_model(
    #             type = type,
    #             model = model,
    #             name = name,
    #             ipadd= ipadd,
    #             location = location,
    #             status = status,
    #             serial_number = serial_number,
    #             os = os,
    #             tagline = tagline,
    #             input_date = input_date,
    #         )
    #         dev_add.save()
    #         dev_id = dev_add.id;
    #         messages.success(request, "Device added succesfully.", extra_tags='alert-success')
    #         return redirect('dev_detail', dev_id=dev_id)
    #     else:
    #         messages.error(request, 'Failed add Device.', extra_tags='alert-danger')
    #         # breadcrumbs
    #         bcitems = [['/home/', 'Home'], ['/devices/', 'Devices'],['/devices/add/', 'Add Device']]
    #         return render(request, 'page-device-add.html', {'title': "Add Device", 'head': "Add Device", 'bcitems': bcitems, 'dev_form': dev_form})
    else:
        trouble_form = TroubleForm()

        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles'],['/troubles/post/', 'Post Link Troubles']]
        return render(request, 'page-trouble-post.html', {'title': "Post Link Troubles", 'head': "Post Link Troubles", 'bcitems': bcitems, 'trouble_form': trouble_form})
