"""falconet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from falconet import forms
from falconet.views import login, home, auth_login, auth_logout, auth_process, get_contacts_type

from netinfo.views import (
sites, site_isp, site_office, site_detail, site_detail_edit, site_add, site_del,
links, link_detail, link_detail_edit, link_add, link_del,
dev, dev_routers, dev_switches, dev_detail, dev_detail_edit, dev_add, dev_del)

from sla.views import (trouble_post, trouble_detail, trouble_active, trouble_inactive)

urlpatterns = [
    #BLANK
    re_path(r'^$', home),
    #ADMIN
    path('admin/', admin.site.urls),
    #HOME
    path('home/', home, name='home'),
    #LOGIN
    path('login/', auth_login, name='login'),
    #LOGOUT
    path('logout/', auth_logout, name='logout'),
    #AUTH
    path('auth/', auth_process, name='auth'),
    #######################################################################################
    #AJAX
    path('ajax/get_contacts_type/', get_contacts_type, name='get_contacts_type'),
    #######################################################################################
    #SITES
    path('sites/', sites, name='sites'),
    #SITES-OFFICE
    path('sites/office/', site_office, name='site_office'),
    #SITES-ISP
    path('sites/isp/', site_isp, name='site_isp'),
    #SITES-DETAIL
    path('sites/<int:site_id>/', site_detail, name='site_detail'),
    #SITES-DETAIL-EDIT
    path('sites/<int:site_id>/edit/', site_detail_edit, name='site_detail_edit'),
    #SITES-ADD
    path('sites/add/', site_add, name='site_add'),
    #SITES-DEL
    path('sites/del/', site_del, name='site_del'),
    #######################################################################################
    #LINKS
    path('links/', links, name='links'),
    #LINKS-DETAIL
    path('links/<int:link_id>/', link_detail, name='link_detail'),
    #LINKS-EDIT
    path('links/<int:link_id>/edit/', link_detail_edit, name='link_detail_edit'),
    #LINKS-ADD
    path('links/add/', link_add, name='link_add'),
    #LINKS-DEL
    path('links/del/', link_del, name='link_del'),
    #######################################################################################
    #DEVICES
    path('devices/', dev, name='dev'),
    #DEVICES-ROUTERS
    path('devices/routers/', dev_routers, name='dev_routers'),
    #DEVICES-SWITCHES
    path('devices/switches/', dev_switches, name='dev_switches'),
    #DEVICES-DETAIL
    path('devices/<int:dev_id>/', dev_detail, name='dev_detail'),
    #DEVICES-DETAIL-EDIT
    path('devices/<int:dev_id>/edit/', dev_detail_edit, name='dev_detail_edit'),
    #DEVICES-ADD
    path('devices/add/', dev_add, name='dev_add'),
    #DEVICES-DEL
    path('devices/del/', dev_del, name='dev_del'),
    #######################################################################################
    #SLA
    #TROUBLE-ACTIVE
    path('troubles/active/', trouble_active, name='trouble_active'),
    #TROUBLE-INACTIVE
    path('troubles/inactive/', trouble_inactive, name='trouble_inactive'),
    #TROUBLE-ADD
    path('troubles/post/', trouble_post, name='trouble_post'),
    #TROUBLE-DETAIL
    path('troubles/<int:trouble_id>/', trouble_detail, name='trouble_detail'),
]
