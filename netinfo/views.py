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

from netinfo.forms import SiteForm, ContactForm, LinkForm, DevForm
from netinfo.models import sites as sites_model, contacts as contacts_model, links as links_model, devices as dev_model

from pprint import pprint

# FUNCTION ONLY
def edit_data(site_post_data, site_db_data):
    site_form = SiteForm(site_post_data, initial=site_db_data)
    if site_form.is_valid():
        if site_form.has_changed():
            for changed_data in site_form.changed_data:
                setattr(site_data, changed_data, site_post_data[changed_data])
                site_data.save()
            messages.success(request, 'Site Information updated succesfully.', extra_tags='alert-success')
            edit_status = 1
        else:
            messages.info(request, 'Site Information not changed.', extra_tags='alert-info')
            edit_status = 1
    else:
        messages.error(request, 'Failed updating Site Information.', extra_tags='alert-danger')
        edit_status = 0
    return edit_status

# Create your views here.
###########################################################################################################################################################################################################################################################################
@login_required()
def sites(request):
    site_data = sites_model.objects.all()

    # link_count = []
    # for site in site_data:
    #     link_count.append(links_model.objects.filter(Q(sites1=site.id)|Q(sites2=site.id)).count())

    # pprint(site_data)
    # pprint(link_count)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/sites/', 'Sites']]
    return render(request, "page-sites.html", {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data})

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
    #site info
    site_data = get_object_or_404(sites_model, id=site_id)
    #contact info
    contacts_data = contacts_model.objects.filter(site = site_id)
    #link info
    links_data = links_model.objects.filter(Q(sites1=site_id)|Q(sites2=site_id))
    #device info
    dev_data = dev_model.objects.filter(location_id = site_id)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/sites/', 'Sites'], [site_id, site_data.name]]
    return render(request, "page-site-detail.html", {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data , 'contacts_data': contacts_data, 'links_data': links_data, 'dev_data': dev_data})

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
    if request.method == 'POST':
        site_post_data = {
            'id':1000,
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

        site_form = SiteForm(site_post_data)

        if site_form.is_valid():
            name = site_form.cleaned_data['name']
            type = site_form.cleaned_data['type']
            location = site_form.cleaned_data['location']
            city = site_form.cleaned_data['city']
            description = site_form.cleaned_data['description']
            ipadd = site_form.cleaned_data['ipadd']
            site_code = site_form.cleaned_data['site_code']
            area_code = site_form.cleaned_data['area_code']
            tagline = site_form.cleaned_data['tagline']

            site_add = sites_model(
                name=name,
                type=type,
                location=location,
                city=city,
                description=description,
                ipadd=ipadd,
                site_code=site_code,
                area_code=area_code,
                tagline=tagline,
            )
            site_add.save()
            site_id = site_add.id;
            messages.success(request, "Site added succesfully.", extra_tags='alert-success')

            if 'add_contact_id' in request.POST:
                contacts_post_add_dataraw = [
                    request.POST.getlist('add_contact_type'),
                    request.POST.getlist('add_contact_number'),
                ]
                contacts_post_add_data=list(map(list, zip(*contacts_post_add_dataraw)))
                for contacts_post_add in contacts_post_add_data:
                    contacts_model(site=sites_model.objects.get(id=int(site_id)), type=contacts_post_add[0], contact_number=contacts_post_add[1]).save()
                    messages.success(request, "Contact: "+contacts_post_add[0]+":"+contacts_post_add[1]+" added succesfully." , extra_tags='alert-success')

            return redirect('site_detail', site_id=site_id)

        else:
            messages.error(request, 'Failed add Site.', extra_tags='alert-danger')
            bcitems = [['/home/', 'Home'], ['/sites/', 'Netadmin'],['/site/add/', 'Add Site']]
            return render(request, 'page-site-add.html', {'title': "Add Site", 'head': "Add Site", 'bcitems': bcitems, 'site_form': site_form})
    else:
        site_form = SiteForm()

        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/sites/', 'Netadmin'],['/site/add/', 'Add Site']]
        return render(request, 'page-site-add.html', {'title': "Add Site", 'head': "Add Site", 'bcitems': bcitems, 'site_form': site_form})

@login_required()
def site_del(request):
    if request.method == 'POST':
        site_id = request.POST['id']
        site_del = get_object_or_404(sites_model, id=site_id)
        site_del.delete()
        messages.success(request, "Site deleted succesfully.", extra_tags='alert-success')
        return redirect('sites')
    else:
        return redirect('sites')
###########################################################################################################################################################################################################################################################################
@login_required()
def links(request):
    link_data = links_model.objects.all()
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/links/', 'Links']]
    return render(request, "page-links.html", {'title': "Links", 'head': "Links", 'bcitems': bcitems, 'link_data': link_data})

@login_required()
def link_add(request):
    if request.method == 'POST':
        link_post_data = {
            'id':1000,
            'sites1':request.POST['sites1'],
            'sites2':request.POST['sites2'],
            'ipadd1':request.POST['ipadd1'],
            'ipadd2':request.POST['ipadd2'],
            'isp':request.POST['isp'],
            'bandwidth':request.POST['bandwidth'],
            'media':request.POST['media'],
            'services':request.POST['services'],
            'status':request.POST['status'],
            'ipadd_others':request.POST['ipadd_others'],
            'vrf_name':request.POST['vrf_name'],
            'links_name':request.POST['links_name'],
            'isp_link_id':request.POST['isp_link_id'],
            'input_date':request.POST['input_date'],
        }

        link_form = LinkForm(link_post_data)

        if link_form.is_valid():
            sites1 = link_form.cleaned_data['sites1']
            sites2 = link_form.cleaned_data['sites2']
            ipadd1 = link_form.cleaned_data['ipadd1']
            ipadd2 = link_form.cleaned_data['ipadd2']
            isp = link_form.cleaned_data['isp']
            bandwidth = link_form.cleaned_data['bandwidth']
            media = link_form.cleaned_data['media']
            services = link_form.cleaned_data['services']
            status = link_form.cleaned_data['status']
            ipadd_others = link_form.cleaned_data['ipadd_others']
            vrf_name = link_form.cleaned_data['vrf_name']
            links_name = link_form.cleaned_data['links_name']
            isp_link_id = link_form.cleaned_data['isp_link_id']
            input_date = link_form.cleaned_data['input_date']

            link_add = links_model(
                sites1 = sites1,
                sites2 = sites2,
                ipadd1 = ipadd1,
                ipadd2 = ipadd2,
                isp = isp,
                bandwidth = bandwidth,
                media = media,
                services = services,
                status = status,
                ipadd_others = ipadd_others,
                vrf_name = vrf_name,
                links_name = links_name,
                isp_link_id = isp_link_id,
                input_date = input_date,
            )
            link_add.save()
            link_id = link_add.id;
            messages.success(request, "Link added succesfully.", extra_tags='alert-success')
            return redirect('link_detail', link_id=link_id)
        else:
            messages.error(request, 'Failed add Link.', extra_tags='alert-danger')
            bcitems = [['/home/', 'Home'], ['/links/', 'Links'],['/links/add/', 'Add Link']]
            return render(request, 'page-link-add.html', {'title': "Add Link", 'head': "Add Link", 'bcitems': bcitems, 'link_form': link_form})
    else:
        link_form = LinkForm()

        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/links/', 'Links'],['/links/add/', 'Add Link']]
        return render(request, 'page-link-add.html', {'title': "Add Link", 'head': "Add Link", 'bcitems': bcitems, 'link_form': link_form})

@login_required()
def link_detail(request, link_id):
    try:
        link_id = int(link_id)
    except ValueError:
        raise Http404()
    link_data = get_object_or_404(links_model, id=link_id)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/links/', 'Links'], [link_id, link_data.links_name]]
    return render(request, "page-link-detail.html", {'title': "Links", 'head': "Links", 'bcitems': bcitems, 'link_data': link_data})

@login_required()
def link_detail_edit(request, link_id):
    if request.method == 'POST':
        # pprint(request.POST)
        # site post intialization
        link_id = int(request.POST['id'])

        link_post_data = {
            'id': request.POST['id'],
            'sites1':request.POST['sites1'],
            'sites2':request.POST['sites2'],
            'ipadd1':request.POST['ipadd1'],
            'ipadd2':request.POST['ipadd2'],
            'isp':request.POST['isp'],
            'bandwidth':request.POST['bandwidth'],
            'media':request.POST['media'],
            'services':request.POST['services'],
            'status':request.POST['status'],
            'ipadd_others':request.POST['ipadd_others'],
            'vrf_name':request.POST['vrf_name'],
            'links_name':request.POST['links_name'],
            'isp_link_id':request.POST['isp_link_id'],
            'input_date':request.POST['input_date'],
        }

        link_data = links_model.objects.get(id=link_id)

        link_db_data = {
            'id': link_data.id,
            'sites1':link_data.sites1,
            'sites2':link_data.sites2,
            'ipadd1':link_data.ipadd1,
            'ipadd2':link_data.ipadd2,
            'isp':link_data.isp,
            'bandwidth':link_data.bandwidth,
            'media':link_data.media,
            'services':link_data.services,
            'status':link_data.status,
            'ipadd_others':link_data.ipadd_others,
            'vrf_name':link_data.vrf_name,
            'links_name':link_data.links_name,
            'isp_link_id':link_data.isp_link_id,
            'input_date':link_data.input_date,
        }
        pprint(link_post_data)
        pprint(link_db_data)
        # link update process
        link_form = LinkForm(link_post_data, initial=link_db_data)
        if link_form.is_valid():
            if link_form.has_changed():
                for changed_data in link_form.changed_data:
                    setattr(link_data, changed_data, link_post_data[changed_data])
                    link_data.save()
                messages.success(request, 'Link data updated succesfully.', extra_tags='alert-success')
                return redirect('link_detail', link_id=link_post_data['id'])
            else:
                messages.info(request, 'Link data not changed.', extra_tags='alert-info')
                return redirect('link_detail', link_id=site_post_data['id'])
        else:
            messages.error(request, 'Failed updating link data.', extra_tags='alert-danger')
            # breadcrumbs
            bcitems = [['/home/', 'Home'], ['/links/', 'Links'], ['/links/'+str(link_id)+'/', link_data.links_name], ['edit', 'Edit']]
            return render(request, 'page-link-detail-edit.html', {'title': "Edit Links", 'head': "Edit Links", 'bcitems': bcitems, 'link_data': link_data, 'link_form': link_form, 'link_id': link_id})
    else:
        try:
            link_id = int(link_id)
        except ValueError:
            raise Http404()
        # site data
        link_data = get_object_or_404(links_model, id=link_id)
        link_form = LinkForm(initial={
            'id': link_data.id,
            'sites1': link_data.sites1,
            'ipadd1': link_data.ipadd1,
            'sites2': link_data.sites2,
            'ipadd2': link_data.ipadd2,
            'isp': link_data.isp,
            'bandwidth': link_data.bandwidth,
            'media': link_data.media,
            'services': link_data.services,
            'status': link_data.status,
            'ipadd_others': link_data.ipadd_others,
            'vrf_name': link_data.vrf_name,
            'links_name': link_data.links_name,
            'isp_link_id': link_data.isp_link_id,
            'input_date': link_data.input_date,
        })
        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/links/', 'Links'], ['/links/'+str(link_id)+'/', link_data.links_name], ['edit', 'Edit']]
        return render(request, 'page-link-detail-edit.html', {'title': "Edit Links", 'head': "Edit Links", 'bcitems': bcitems, 'link_data': link_data, 'link_form': link_form, 'link_id': link_id})

@login_required()
def link_del(request):
    if request.method == 'POST':
        link_id = request.POST['id']
        link_del = get_object_or_404(links_model, id=link_id)
        link_del.delete()
        messages.success(request, "Link deleted succesfully.", extra_tags='alert-success')
        return redirect('links')
    else:
        return redirect('links')

###########################################################################################################################################################################################################################################################################
@login_required()
def dev(request):
    dev_data = dev_model.objects.all()
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/devices/', 'Devices']]
    return render(request, "page-devices.html", {'title': "Devices", 'head': "Devices", 'bcitems': bcitems, 'dev_data': dev_data})

@login_required()
def dev_routers(request):
    dev_data = dev_model.objects.filter(type= 'router')
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/devices/', 'Devices'], ['/devices/routers/', 'Routers']]
    return render(request, "page-devices.html", {'title': "Devices", 'head': "Devices", 'bcitems': bcitems, 'dev_data': dev_data})

@login_required()
def dev_switches(request):
    dev_data = dev_model.objects.filter(type= 'switch')
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/devices/', 'Devices'], ['/devices/switches/', 'Switches']]
    return render(request, "page-devices.html", {'title': "Devices", 'head': "Devices", 'bcitems': bcitems, 'dev_data': dev_data})

@login_required()
def dev_add(request):
    if request.method == 'POST':
        # pprint(request.POST)
        dev_post_data = {
            'id':1000,
            'type':request.POST['type'],
            'model':request.POST['model'],
            'name':request.POST['name'],
            'ipadd':request.POST['ipadd'],
            'location':request.POST['location'],
            'status':request.POST['status'],
            'serial_number':request.POST['serial_number'],
            'os':request.POST['os'],
            'tagline':request.POST['tagline'],
            'input_date':request.POST['input_date'],
        }
        # pprint(dev_post_data)

        dev_form = DevForm(dev_post_data)

        if dev_form.is_valid():
            type = dev_form.cleaned_data['type']
            model = dev_form.cleaned_data['model']
            name = dev_form.cleaned_data['name']
            ipadd = dev_form.cleaned_data['ipadd']
            location =dev_form.cleaned_data['location']
            status = dev_form.cleaned_data['status']
            serial_number = dev_form.cleaned_data['serial_number']
            os = dev_form.cleaned_data['os']
            tagline = dev_form.cleaned_data['tagline']
            input_date = dev_form.cleaned_data['input_date']

            dev_add = dev_model(
                type = type,
                model = model,
                name = name,
                ipadd= ipadd,
                location = location,
                status = status,
                serial_number = serial_number,
                os = os,
                tagline = tagline,
                input_date = input_date,
            )
            dev_add.save()
            dev_id = dev_add.id;
            messages.success(request, "Device added succesfully.", extra_tags='alert-success')
            return redirect('dev_detail', dev_id=dev_id)
        else:
            messages.error(request, 'Failed add Device.', extra_tags='alert-danger')
            # breadcrumbs
            bcitems = [['/home/', 'Home'], ['/devices/', 'Devices'],['/devices/add/', 'Add Device']]
            return render(request, 'page-device-add.html', {'title': "Add Device", 'head': "Add Device", 'bcitems': bcitems, 'dev_form': dev_form})
    else:
        dev_form = DevForm()

        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/devices/', 'Devices'],['/devices/add/', 'Add Device']]
        return render(request, 'page-device-add.html', {'title': "Add Device", 'head': "Add Device", 'bcitems': bcitems, 'dev_form': dev_form})

@login_required()
def dev_detail(request, dev_id):
    try:
        dev_id = int(dev_id)
    except ValueError:
        raise Http404()
    dev_data = get_object_or_404(dev_model, id=dev_id)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/devices/', 'Devices'], [dev_id, dev_data.name]]
    return render(request, "page-device-detail.html", {'title': "Devices", 'head': "Devices", 'bcitems': bcitems, 'dev_data': dev_data})

@login_required()
def dev_detail_edit(request, dev_id):
    if request.method == 'POST':
        # pprint(request.POST)
        # site post intialization
        dev_id = int(request.POST['id'])

        dev_post_data = {
            'id':request.POST['id'],
            'type':request.POST['type'],
            'model':request.POST['model'],
            'name':request.POST['name'],
            'ipadd':request.POST['ipadd'],
            'location':request.POST['location'],
            'status':request.POST['status'],
            'serial_number':request.POST['serial_number'],
            'os':request.POST['os'],
            'tagline':request.POST['tagline'],
            'input_date':request.POST['input_date'],
        }

        dev_data = dev_model.objects.get(id=dev_id)

        dev_db_data = {
            'id':dev_data.id,
            'type':dev_data.type,
            'model':dev_data.model,
            'name':dev_data.name,
            'ipadd':dev_data.ipadd,
            'location':dev_data.location,
            'status':dev_data.status,
            'serial_number':dev_data.serial_number,
            'os':dev_data.os,
            'tagline':dev_data.tagline,
            'input_date':dev_data.input_date,
        }

        pprint(dev_post_data)
        pprint(dev_db_data)
        # link update process
        dev_form = DevForm(dev_post_data, initial=dev_db_data)
        if dev_form.is_valid():
            if dev_form.has_changed():
                for changed_data in dev_form.changed_data:
                    setattr(dev_data, changed_data, dev_post_data[changed_data])
                    dev_data.save()
                messages.success(request, 'Device data updated succesfully.', extra_tags='alert-success')
                return redirect('dev_detail', dev_id=dev_post_data['id'])
            else:
                messages.info(request, 'Device data not changed.', extra_tags='alert-info')
                return redirect('dev_detail', dev_id=dev_post_data['id'])
        else:
            messages.error(request, 'Failed updating device data.', extra_tags='alert-danger')
            # breadcrumbs
            bcitems = [['/home/', 'Home'], ['/devices/', 'Devices'], ['/devices/'+str(dev_id)+'/', dev_data.name], ['edit', 'Edit']]
            return render(request, 'page-device-detail-edit.html', {'title': "Edit Device", 'head': "Edit Device", 'bcitems': bcitems, 'dev_data': dev_data, 'dev_form': dev_form, 'dev_id': dev_id})
    else:
        try:
            dev_id = int(dev_id)
        except ValueError:
            raise Http404()
        # dev data
        dev_data = get_object_or_404(dev_model, id=dev_id)
        # pprint(dev_data)
        dev_form = DevForm(initial={
            'id':dev_data.id,
            'type':dev_data.type,
            'model':dev_data.model,
            'name':dev_data.name,
            'ipadd':dev_data.ipadd,
            'location':dev_data.location,
            'status':dev_data.status,
            'serial_number':dev_data.serial_number,
            'os':dev_data.os,
            'tagline':dev_data.tagline,
            'input_date':dev_data.input_date,
        })
        # breadcrumbs
        bcitems = [['/home/', 'Home'], ['/devices/', 'Devices'], ['/devices/'+str(dev_id)+'/', dev_data.name], ['edit', 'Edit']]
        return render(request, 'page-device-detail-edit.html', {'title': "Edit Device", 'head': "Edit Device", 'bcitems': bcitems, 'dev_data': dev_data, 'dev_form': dev_form, 'dev_id': dev_id})

@login_required()
def dev_del(request):
    if request.method == 'POST':
        dev_id = request.POST['id']
        dev_del = get_object_or_404(dev_model, id=dev_id)
        dev_del.delete()
        messages.success(request, "Device deleted succesfully.", extra_tags='alert-success')
        return redirect('dev')
    else:
        return redirect('dev')
