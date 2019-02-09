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
def troubles(request):
    trouble_data = troubles_model.objects.all()
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles']]
    return render(request, "page-troubles.html", {'title': "Troubles", 'head': "Troubles", 'bcitems': bcitems, 'trouble_data': trouble_data})

@login_required()
def trouble_active(request):
    trouble_data = troubles_model.objects.filter(status = 1)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles'], ['active', 'Active']]
    return render(request, "page-troubles.html", {'title': "Troubles", 'head': "Troubles", 'bcitems': bcitems, 'trouble_data': trouble_data})

@login_required()
def trouble_inactive(request):
    trouble_data = troubles_model.objects.filter(status = 0)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles'], ['inactive', 'Inactive']]
    return render(request, "page-troubles.html", {'title': "Troubles", 'head': "Troubles", 'bcitems': bcitems, 'trouble_data': trouble_data})

@login_required()
def trouble_detail(request, trouble_id):
    try:
        trouble_id = int(trouble_id)
    except ValueError:
        raise Http404()
    trouble_data = get_object_or_404(troubles_model, id=trouble_id)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles'], [trouble_id, trouble_data.link.links_name+'('+str(trouble_data.id)+')']]
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
            'link':request.POST['link'],
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
            link = trouble_form.cleaned_data['link']
            cause_type = trouble_form.cleaned_data['cause_type']
            start_time = trouble_form.cleaned_data['start_time']
            end_time = trouble_form.cleaned_data['end_time']
            status = trouble_status
            description = trouble_form.cleaned_data['description']
            user = request.user
            isp_ticket = trouble_form.cleaned_data['isp_ticket']

            trouble_post = troubles_model(
                link = link,
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

@login_required()
def trouble_detail_edit(request, trouble_id):
    if request.method == 'POST':
        # pprint(request.POST)
        if request.POST['end_time'] == '':
            trouble_status = 1
            end_time = None
        else:
            trouble_status = 0
            end_time = request.POST['end_time']

        pprint(trouble_status)

        trouble_id = int(request.POST['id'])

        trouble_data = troubles_model.objects.get(id=trouble_id)

        trouble_post_data = {
            'id':request.POST['id'],
            'link':request.POST['link'],
            'cause_type':request.POST['cause_type'],
            'start_time':request.POST['start_time'],
            'end_time':end_time,
            'status':trouble_status,
            'description':request.POST['description'],
            'user': trouble_data.user,
            'isp_ticket':request.POST['isp_ticket'],
        }

        trouble_db_data = {
            'id':trouble_data.id,
            'link':trouble_data.link,
            'cause_type':trouble_data.cause_type,
            'start_time':trouble_data.start_time,
            'end_time':trouble_data.end_time,
            'status':trouble_data.status,
            'description':trouble_data.description,
            'user': trouble_data.user,
            'isp_ticket':trouble_data.isp_ticket,
        }

        pprint(trouble_post_data)
        pprint(trouble_db_data)

        # Trouble data update process
        trouble_form = TroubleForm(trouble_post_data, initial=trouble_db_data)
        if trouble_form.is_valid():
            if trouble_form.has_changed():
                for changed_data in trouble_form.changed_data:
                    setattr(trouble_data, changed_data, trouble_post_data[changed_data])
                    trouble_data.save()
                messages.success(request, 'Link trouble data updated succesfully.', extra_tags='alert-success')
                return redirect('trouble_detail', trouble_id=trouble_post_data['id'])
            else:
                messages.info(request, 'Link trouble data not changed.', extra_tags='alert-info')
                return redirect('trouble_detail', trouble_id=trouble_post_data['id'])
        else:
            messages.error(request, 'Failed updating link trouble data.', extra_tags='alert-danger')
            # breadcrumbs
            bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles'],['/troubles/'+str(trouble_id)+'/Edit/', trouble_data.link.links_name+'('+str(trouble_data.id)+')'], ['edit', 'Edit']]
            return render(request, 'page-trouble-detail-edit.html', {'title': "Edit Trouble", 'head': "Edit Trouble", 'bcitems': bcitems, 'trouble_data': trouble_data, 'trouble_form': trouble_form, 'trouble_id': trouble_id})
    else:
        try:
            trouble_id = int(trouble_id)
        except ValueError:
            raise Http404()
        # dev data
        trouble_data = get_object_or_404(troubles_model, id=trouble_id)
        # pprint(dev_data)
        trouble_form = TroubleForm(initial={
            'id':trouble_data.id,
            'link':trouble_data.link,
            'cause_type':trouble_data.cause_type,
            'start_time':trouble_data.start_time,
            'end_time':trouble_data.end_time,
            'status':trouble_data.status,
            'description':trouble_data.description,
            'user': trouble_data.user,
            'isp_ticket':trouble_data.isp_ticket,

        })
        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/troubles/', 'Troubles'],['/troubles/'+str(trouble_id)+'/Edit/', trouble_data.link.links_name+'('+str(trouble_data.id)+')'], ['edit', 'Edit']]
        return render(request, 'page-trouble-detail-edit.html', {'title': "Edit Trouble", 'head': "Edit Trouble", 'bcitems': bcitems, 'trouble_data': trouble_data, 'trouble_form': trouble_form, 'trouble_id': trouble_id})
