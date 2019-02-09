import datetime

from django.db import models
from django.contrib.auth.models import User
from netinfo.models import links

# Create your models here.

class troubles(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.ForeignKey(links, on_delete=models.CASCADE, null=False)
    cause_type = models.CharField(max_length=50, null=False)
    start_time = models.DateTimeField(default=datetime.datetime.now, null=False)
    end_time = models.DateTimeField(null=True)
    status = models.IntegerField(default=1)
    description = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isp_ticket = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "troubles"

    def __str__(self):
        return u'%s %s %s' %(self.id, self.link_id, self.status)
