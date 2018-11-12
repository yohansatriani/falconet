from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from falconet import views
from falconet.forms import LoginForm

from netinfo.forms import SiteForm
from netinfo.models import sites as sites_model, contacts as contacts_model


# Create your views here.
@login_required()
def sites(request):
    site_data = sites_model.objects.all()
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/sites/', 'Sites']]
    html = render_to_string('page-sites.html', {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data })
    return HttpResponse(html)

@login_required()
def site_office(request):
    site_data = sites_model.objects.filter(type__in = ['HO', 'KC', 'KCP', 'KK'])
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/sites/', 'Sites'], ['/office/', 'Office']]
    html = render_to_string('page-sites.html', {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data })
    return HttpResponse(html)

@login_required()
def site_isp(request):
    site_data = sites_model.objects.filter(type__in = ['ISP', 'POP'])
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/sites/', 'Sites'], ['isp', 'ISP']]
    html = render_to_string('page-sites.html', {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data })
    return HttpResponse(html)

@login_required()
def site_detail(request, site_id):
    try:
        site_id = int(site_id)
    except ValueError:
        raise Http404()
    site_data = get_object_or_404(sites_model, id=site_id) 
    contacts_data = contacts_model.objects.filter(site = site_id)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/sites/', 'Sites'], [site_id, site_data.name]]
    return render(request, "page-site-detail.html", {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data ,'contacts_data': contacts_data})

@login_required()
def site_detail_edit(request, site_id):    
    if request.method == 'POST':
        site_id = int(request.POST['id'])
        # contact data & type
        contacts_type = contacts_model.objects.values('type').distinct()
        contacts_data = contacts_model.objects.filter(site = site_id)
        
        site_post_data = {
            'id': request.POST['id'],
            'name':request.POST['name'],
            'description':request.POST['description'],
            'type':request.POST['type'],
            'location':request.POST['location'],
            'city':request.POST['city'],
            'site_code':request.POST['site_code'],
            'area_code':request.POST['area_code'],
            'ipadd':request.POST['ipadd'],
            'tagline':request.POST['tagline']
        }
        
        site_data = sites_model.objects.get(id=int(request.POST['id']))

        site_db_data = {
            'id': site_data.id,
            'name': site_data.name,
            'description':site_data.description,
            'type': site_data.type,
            'location': site_data.location,
            'city': site_data.city,
            'site_code': site_data.site_code,
            'area_code': site_data.area_code,
            'ipadd': site_data.ipadd,
            'tagline': site_data.tagline,
        }
        
        site_form = SiteForm(site_post_data, initial=site_db_data)
        
        if site_form.is_valid():
            if site_form.has_changed():
                for changed_data in site_form.changed_data:
                    setattr(site_data, changed_data, site_post_data[changed_data])
                    site_data.save()
                
                messages.success(request, 'Data updated succesfully.', extra_tags='alert-success')
                return redirect('site_detail', site_id=site_post_data['id'])
            else:
                messages.info(request, 'No data changed.', extra_tags='alert-info')
                return redirect('site_detail', site_id=site_post_data['id'])
        else:
            messages.error(request, 'Failed updating data.', extra_tags='alert-danger')
            # breadcrumbs
            bcitems = [['/home/', 'Home'], ['/sites/', 'Sites'], ['/sites/'+str(site_id)+'/', site_data.name],['edit', 'Edit']]
            return render(request, 'page-site-detail-edit.html', {'title': "Edit Sites", 'head': "Edit Sites", 'bcitems': bcitems, 'contacts_data': contacts_data, 'contacts_type': contacts_type, 'site_form': site_form, 'site_id': site_id})
    else:
        try:
            site_id = int(site_id)
        except ValueError:
            raise Http404()
        site_data = get_object_or_404(sites_model, id=site_id)
        site_form = SiteForm(initial={
            'id': site_data.id,
            'name': site_data.name,
            'description':site_data.description,
            'type': site_data.type,
            'location': site_data.location,
            'city': site_data.city,
            'site_code': site_data.site_code,
            'area_code': site_data.area_code,
            'ipadd': site_data.ipadd,
            'tagline': site_data.tagline,
        })
        # contact data & type
        contacts_type = contacts_model.objects.values('type').distinct()
        contacts_data = contacts_model.objects.filter(site = site_id)
        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/sites/', 'Sites'], ['/sites/'+str(site_id)+'/', site_data.name],['edit', 'Edit']]
        return render(request, 'page-site-detail-edit.html', {'title': "Edit Sites", 'head': "Edit Sites", 'bcitems': bcitems, 'contacts_data': contacts_data, 'contacts_type': contacts_type, 'site_form': site_form, 'site_id': site_id})