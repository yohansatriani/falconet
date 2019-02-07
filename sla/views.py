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

from sla.forms import TroubleForm
from sla.models import troubles as troubles_model

from pprint import pprint
# Create your views here.

@login_required()
def trouble_active(request):
    trouble_data = troubles_model.objects.filter(status = 1)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles']]
    return render(request, "page-troubles.html", {'title': "Troubles", 'head': "Troubles", 'bcitems': bcitems, 'trouble_data': trouble_data})

@login_required()
def trouble_inactive(request):
    trouble_data = troubles_model.objects.filter(status = 0)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles']]
    return render(request, "page-troubles.html", {'title': "Troubles", 'head': "Troubles", 'bcitems': bcitems, 'trouble_data': trouble_data})

@login_required()
def trouble_detail(request, trouble_id):
    try:
        trouble_id = int(trouble_id)
    except ValueError:
        raise Http404()
    trouble_data = get_object_or_404(troubles_model, id=trouble_id)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles'], [trouble_id, trouble_data.link_id.links_name]]
    return render(request, "page-trouble-detail.html", {'title': "Troubles", 'head': "Troubles", 'bcitems': bcitems, 'trouble_data': trouble_data})

@login_required()
def trouble_post(request):
    if request.method == 'POST':
        pprint(request.POST)

        if request.POST['end_time'] == '':
            trouble_status = 1
        else:
            trouble_status = 0

        trouble_post_data = {
            'id':1000,
            'link_id':request.POST['link_id'],
            'cause_type':request.POST['cause_type'],
            'start_time':request.POST['start_time'],
            'end_time':request.POST['end_time'],
            'status':trouble_status,
            'description':request.POST['description'],
            'user': request.user,
            'isp_ticket':request.POST['isp_ticket'],
        }

        pprint(trouble_status)

        trouble_form = TroubleForm(trouble_post_data)

        if trouble_form.is_valid():
            link_id = trouble_form.cleaned_data['link_id']
            cause_type = trouble_form.cleaned_data['cause_type']
            start_time = trouble_form.cleaned_data['start_time']
            end_time = trouble_form.cleaned_data['end_time']
            status = trouble_status
            description = trouble_form.cleaned_data['description']
            user = request.user
            isp_ticket = trouble_form.cleaned_data['isp_ticket']

            trouble_post = troubles_model(
                link_id = link_id,
                cause_type = cause_type,
                start_time = start_time,
                end_time = end_time,
                status = status,
                description = description,
                user = user,
                isp_ticket = isp_ticket,
            )

            trouble_post.save()
            trouble_id = trouble_post.id;
            messages.success(request, "Link trouble added succesfully.", extra_tags='alert-success')
            return redirect('trouble_detail', trouble_id=trouble_id)
        else:
            messages.error(request, 'Failed post link trouble.', extra_tags='alert-danger')
            # breadcrumbs
            bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles'],['/troubles/post/', 'Post Link Troubles']]
            return render(request, 'page-trouble-post.html', {'title': "Post Link Troubles", 'head': "Post Link Troubles", 'bcitems': bcitems, 'trouble_form': trouble_form})
    else:
        trouble_form = TroubleForm()

        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles'],['/troubles/post/', 'Post Link Troubles']]
        return render(request, 'page-trouble-post.html', {'title': "Post Link Troubles", 'head': "Post Link Troubles", 'bcitems': bcitems, 'trouble_form': trouble_form})
