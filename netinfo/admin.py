from django.contrib import admin

# Register your models here.
from .models import sites, contacts, links, devices

admin.site.register(sites)
admin.site.register(contacts)
admin.site.register(links)
admin.site.register(devices)
