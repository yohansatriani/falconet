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
from falconet.views import login, home, auth


urlpatterns = [
    #ADMIN
    path('admin/', admin.site.urls),
    #HOME
    path('home/', home),
    #AUTH_VIEWS.LOGIN
    path('login/', auth_views.login, {
        'template_name': 'page-login.html',
        'authentication_form': forms.LoginForm,
        'extra_context': {
                'title': 'Login',
                'head': 'Login',
            },
        },
    ),
    #AUTH
    path('auth/', auth),
]
