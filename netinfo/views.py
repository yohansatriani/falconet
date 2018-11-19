from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from falconet import views
from falconet.forms import LoginForm

from netinfo.forms import SiteForm, ContactForm
from netinfo.models import sites as sites_model, contacts as contacts_model

from pprint import pprint

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
        # site post intialization
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

        # contact post update process
        if 'contact_id' in request.POST:
            contacts_post_data_raw = [
                request.POST.getlist('contact_id'),
                request.POST.getlist('contact_type'),
                request.POST.getlist('contact_number'),
            ]
            # transpose post data
            contacts_post_data_zip=list(map(list, zip(*contacts_post_data_raw)))

            for contacts_post_data_list in contacts_post_data_zip:
                contacts_data = contacts_model.objects.get(id=contacts_post_data_list[0])
                contacts_db_data = {
                    'contact_id': contacts_data.id,
                    'contact_type': contacts_data.type,
                    'contact_number':contacts_data.contact_number,
                }
                contacts_post_data = {
                    'contact_id': contacts_post_data_list[0],
                    'contact_type': contacts_post_data_list[1],
                    'contact_number': contacts_post_data_list[2],
                }
                contact_form = ContactForm(contacts_post_data, initial=contacts_db_data)
                if contact_form.is_valid():
                    if contact_form.has_changed():
                        for changed_data in contact_form.changed_data:
                            setattr(contacts_data, changed_data, contacts_post_data[changed_data])
                            contacts_data.save()
                        messages.success(request, "Contact: "+contacts_post_data['contact_type'].title()+":"+contacts_post_data['contact_number']+" updated succesfully.", extra_tags='alert-success')
                    else:
                        messages.info(request, "Contact: "+contacts_post_data['contact_type'].title()+":"+contacts_post_data['contact_number']+" not changed.", extra_tags='alert-info')
                else:
                    messages.error(request, 'Failed updating contact'+contacts_post_data['contact_type'].title()+":"+contacts_post_data['contact_number'], extra_tags='alert-danger')

        # contact post delete process
        if 'del_contact_id' in request.POST:
            contacts_post_del_id = request.POST.getlist('del_contact_id')

            for del_id in contacts_post_del_id:
                contacts_data = contacts_model.objects.get(id=del_id)
                messages.success(request, "Contact: "+contacts_data.type+":"+contacts_data.contact_number+" deleted succesfully.", extra_tags='alert-success')
                contacts_data.delete()

        # contact post add process
        if 'add_contact_id' in request.POST:
            contacts_post_add_dataraw = [
                request.POST.getlist('add_contact_type'),
                request.POST.getlist('add_contact_number'),
            ]

            contacts_post_add_data=list(map(list, zip(*contacts_post_add_dataraw)))

            for contacts_post_add in contacts_post_add_data:
                contacts_model(site=sites_model.objects.get(id=site_id), type=contacts_post_add[0], contact_number=contacts_post_add[1]).save()
                messages.success(request, "Contact: "+contacts_post_add[0]+":"+contacts_post_add[1]+" added succesfully.", extra_tags='alert-success')

        # site update process
        site_form = SiteForm(site_post_data, initial=site_db_data)
        if site_form.is_valid():
            if site_form.has_changed():
                for changed_data in site_form.changed_data:
                    setattr(site_data, changed_data, site_post_data[changed_data])
                    site_data.save()
                messages.success(request, 'Site Information updated succesfully.', extra_tags='alert-success')
                return redirect('site_detail', site_id=site_post_data['id'])
            else:
                messages.info(request, 'Site Information not changed.', extra_tags='alert-info')
                return redirect('site_detail', site_id=site_post_data['id'])
        else:
            messages.error(request, 'Failed updating Site Information.', extra_tags='alert-danger')
            # breadcrumbs
            bcitems = [['/home/', 'Home'], ['/sites/', 'Sites'], ['/sites/'+str(site_id)+'/', site_data.name],['edit', 'Edit']]
            return render(request, 'page-site-detail-edit.html', {'title': "Edit Sites", 'head': "Edit Sites", 'bcitems': bcitems, 'contacts_data': contacts_data, 'contacts_type': contacts_type, 'site_form': site_form, 'site_id': site_id})
    else:
        try:
            site_id = int(site_id)
        except ValueError:
            raise Http404()
        # site data
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
        # contact type & number
        contacts_type = contacts_model.objects.values('type').distinct()
        contacts_data = contacts_model.objects.filter(site = site_id)
        contacts_form = []
        if contacts_data:
            for contact in contacts_data:
                contacts_form.append(ContactForm(auto_id='%s_'+str(contact.id), initial={
                    'contact_id': contact.id,
                    # 'site_id': contact.site,
                    'contact_type': contact.type,
                    'contact_number': contact.contact_number
                }))
        else:
            contact_form = False
        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/sites/', 'Sites'], ['/sites/'+str(site_id)+'/', site_data.name],['edit', 'Edit']]
        return render(request, 'page-site-detail-edit.html', {'title': "Edit Sites", 'head': "Edit Sites", 'bcitems': bcitems, 'contacts_form': contacts_form, 'contacts_data': contacts_data, 'contacts_type': contacts_type, 'site_form': site_form, 'site_id': site_id})

@login_required()
def site_add(request):
    site_form = SiteForm()

    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/sites/', 'Netadmin'],['/netadmin/addsite/', 'Add Site']]
    return render(request, 'page-admin-addsite.html', {'title': "Add Site", 'head': "Add Site", 'bcitems': bcitems, 'site_form': site_form})
