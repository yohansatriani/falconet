from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.http import HttpResponse

def home(request):
    html = render_to_string('page-login.html', {'title': "Login", 'head': "Login"})
    return HttpResponse(html)

def auth(request):
    html = render_to_string('page-home.html', {'title': "Authentication", 'head': "Authentication"})
    return HttpResponse(html)