from django.contrib import admin
from .models import sites, contacts, links, devices

# Register your models here.

admin.site.register(sites)
admin.site.register(contacts)
admin.site.register(links)
admin.site.register(devices)
