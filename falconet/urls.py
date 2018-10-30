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
from django.urls import path
from django.contrib.auth import views as auth_views

from falconet import forms
from falconet.views import login, home, sites, site_office, site_isp, site_detail, site_detail_edit, auth_login, auth_logout, auth_process


urlpatterns = [
    #ADMIN
    path('admin/', admin.site.urls),
    #HOME
    path('home/', home, name='home'),
    #SITES
    path('sites/', sites, name='sites'),
    #SITES-OFFICE
    path('sites/office/', site_office, name='site_office'),
    #SITES-ISP
    path('sites/isp/', site_isp, name='site_isp'),
    #SITES-DETAIL
    path('sites/<int:site_id>/', site_detail, name='site_detail'),
    #SITES-DETAIL-EDUT
    path('sites/<int:site_id>/edit/', site_detail_edit, name='site_detail_edit'),
    #LOGIN
    path('login/', auth_login, name='login'),
    #LOGOUT
    path('logout/', auth_logout, name='logout'),
    #AUTH
    path('auth/', auth_process, name='auth'),
]
