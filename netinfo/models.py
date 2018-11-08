from django.db import models

# Create your models here.

class sites(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)  
    type = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=300, default='')
    city = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, default='')
    ipadd = models.CharField(max_length=100, default='0.0.0.0/0')
    site_code = models.CharField(max_length=3, default='')
    area_code = models.CharField(max_length=3, default='')
    tagline = models.CharField(max_length=500, default='')
    
    class Meta:
        verbose_name_plural = "sites"
        
    def __str__(self):
        return u'%s %s %s %s %s %s %s %s %s %s' %(self.id, self.name, self.type, self.location, self.city, self.description, self.ipadd, self.site_code, self.area_code, self.tagline)

class contacts(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(sites, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, default='')
    contact_number = models.CharField(max_length=50, default='')
    
    class Meta:
        verbose_name_plural = "contacts"
    
    def __str__(self):
        return u'%s %s' %(self.site, self.type)

class links(models.Model):
    id = models.AutoField(primary_key=True)
    sites1 = models.ForeignKey(sites, on_delete=models.CASCADE, related_name='sites1')
    sites2 = models.ForeignKey(sites, on_delete=models.CASCADE, related_name='sites2')   
    ipadd1 = models.CharField(max_length=19, default='0.0.0.0/0')
    ipadd2 = models.CharField(max_length=19, default='0.0.0.0/0')  
    isp = models.CharField(max_length=20, default='unknown')
    bandwidth = models.PositiveIntegerField(default=0)
    media = models.CharField(max_length=20, default='unknown')
    services = models.CharField(max_length=10, default='unknown')
    status = models.BooleanField(max_length=1, default=1)
    ipadd_others = models.CharField(max_length=19, null=True)
    vrf_name = models.CharField(max_length=100, null=True)
    links_name = models.CharField(max_length=100, null=True)
    isp_link_id = models.CharField(max_length=20, null=True)
    input_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "links"
    
    def __str__(self):
        return u'%s %s' %(self.sites1, self.isp)