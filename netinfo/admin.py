from django.contrib import admin

# Register your models here.
from .models import sites, contacts, links

admin.site.register(sites)
admin.site.register(contacts)
admin.site.register(links)