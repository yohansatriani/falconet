from django import forms
from netinfo.models import sites
from django.forms import ModelChoiceField

class SiteModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name

class SiteForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'id', 'name':'id'})
    )
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'name', 'name':'name'})
    )
    SITE_TYPE = (('PP', 'PP'),('KK', 'KK'),('KCP', 'KCP'),('KC', 'KC'),('HO', 'HO'),('DRC', 'DRC'),('ISP', 'ISP'),('PARTNER', 'PARTNER'))
    type = forms.ChoiceField(
        label="Type",
        choices=SITE_TYPE,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'type', 'name':'type'})
    )
    location = forms.CharField(
        label="Location",
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'location', 'name':'location', 'rows':3})
    )
    SITE_CITY = (('All City', 'All City'),('Yogyakarta', 'Yogyakarta'),('Gunungkidul', 'Gunungkidul'),('Kulon Progo', 'Kulon Progo'),('Bantul', 'Bantul'),('Sleman', 'Sleman'))
    city = forms.ChoiceField(
        label="City",
        choices=SITE_CITY,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'city', 'name':'city'})
    )
    description = forms.CharField(
        label="Description",
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'description', 'name':'description', 'rows':2})
    )
    ipadd = forms.CharField(
        label="IP Address",
        max_length=100,
        required=False,
        help_text='Example : 192.168.1.1 or 192.168.1.0/24',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'ipadd', 'name':'ipadd', 'pattern': '^(([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5])((/[0-9]|/[1-2][0-9]|/[1-3][0-2])?)$'})
    )
    site_code = forms.CharField(
        label="Site code",
        max_length=3,
        required=False,
        help_text='Input 3 digits site code',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'site_code', 'name':'site_code', 'pattern': '\d{3}'})
    )
    area_code = forms.CharField(
        label="Area code",
        max_length=3,
        required=False,
        help_text='Input 3 digits area code',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'area_code', 'name':'area_code', 'pattern': '\d{3}'})
    )
    tagline = forms.CharField(
        label="Tagline",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'tagline', 'name':'tagline', 'rows':2})
    )

class ContactForm(forms.Form):
    contact_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'name':'contact_id'})
    )
    CONTACT_TYPE = (('phone', 'PHONE'),('fax', 'FAX'))
    contact_type = forms.ChoiceField(
        label="Type",
        choices=CONTACT_TYPE,
        widget=forms.Select(attrs={'class': 'col-sm-3 form-control', 'name':'contact_type'})
    )
    contact_number = forms.CharField(
        label="Number",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name':'contact_number', 'pattern': '^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$'})
    )

class LinkForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'id', 'name':'id'})
    )
    sites1 = SiteModelChoiceField(
        queryset=sites.objects.all(),
        empty_label="--Please-Select--",
        label="Site-1",
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'sites1', 'name':'sites1'})
    )
    ipadd1 = forms.CharField(
        label="IP WAN-1",
        max_length=19,
        required=False,
        help_text='Example : 192.168.1.1 or 192.168.1.0/24',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'ipadd1', 'name':'ipadd2', 'pattern': '^(([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5])((/[0-9]|/[1-2][0-9]|/[1-3][0-2])?)$'})
    )
    sites2 = SiteModelChoiceField(
        queryset=sites.objects.all(),
        empty_label="--Please-Select--",
        label="Site-2",
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'sites2', 'name':'sites2'})
    )
    ipadd2 = forms.CharField(
        label="IP WAN-2",
        max_length=19,
        required=False,
        help_text='Example : 192.168.1.1 or 192.168.1.0/24',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'ipadd1', 'name':'ipadd2', 'pattern': '^(([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5])((/[0-9]|/[1-2][0-9]|/[1-3][0-2])?)$'})
    )
    ISP_LIST = (('Telkom', 'Telkom'),('Lintasarta', 'Lintasarta'),('ICON+', 'ICON+'))
    isp = forms.ChoiceField(
        label="ISP",
        choices=ISP_LIST,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'isp', 'name':'isp'})
    )
    bandwidth = forms.IntegerField(
        label="Bandwidth",
        help_text='in kbps(kilobit/second)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'bandwidth', 'name':'bandwidth'})
    )
    MEDIA_LIST = (('FO', 'Fibre Optic'),('BWA', 'BWA'),('VSAT', 'VSAT'))
    media = forms.ChoiceField(
        label="Media",
        choices=MEDIA_LIST,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'media', 'name':'media'})
    )
    SERVICE_LIST = (('MPLS', 'MPLS'),('Metro Ethernet', 'Metro Ethernet'))
    services = forms.ChoiceField(
        label="Service",
        choices=SERVICE_LIST,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'services', 'name':'services'})
    )
    STATUS_LIST = ((1, 'Enabled'),(0, 'Disabled'))
    status = forms.ChoiceField(
        label="Status",
        choices=STATUS_LIST,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'status', 'name':'status'})
    )
    ipadd_others = forms.CharField(
        label="Additional IP",
        max_length=19,
        required=False,
        help_text='Example : 192.168.1.1 or 192.168.1.0/24',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'ipadd_others', 'name':'ipadd_others', 'pattern': '^(([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5])((/[0-9]|/[1-2][0-9]|/[1-3][0-2])?)$'})
    )
    vrf_name = forms.CharField(
        label="VRF",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'vrf_name', 'name':'vrf_name'})
    )
    links_name = forms.CharField(
        label="Link Name",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'links_name', 'name':'links_name'})
    )
    isp_link_id = forms.CharField(
        label="ISP Link ID",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'isp_link_id', 'name':'isp_link_id'})
    )
    input_date = forms.DateTimeField(
        label="Date Added",
        widget=forms.DateInput(format='%m/%d/%Y',attrs={'class': 'form-control', 'id' : 'datepicker', 'name':'input_date'})
    )

class DevForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'id', 'name':'id'})
    )
    DEV_TYPE = (('router', 'Router'),('switch', 'Switch'),('web application firewall', 'WAF'))
    type = forms.ChoiceField(
        label="Type",
        choices=DEV_TYPE,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'type', 'name':'type'})
    )
    model = forms.CharField(
        label="Model",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'model', 'name':'model'})
    )
    name = forms.CharField(
        label="Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'name', 'name':'name'})
    )
    ipadd = forms.CharField(
        label="IP Address",
        max_length=19,
        required=False,
        help_text='Example : 192.168.1.1 or 192.168.1.0/24',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'ipadd', 'name':'ipadd', 'pattern': '^(([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5])((/[0-9]|/[1-2][0-9]|/[1-3][0-2])?)$'})
    )
    location = SiteModelChoiceField(
        queryset=sites.objects.all(),
        empty_label="--Please-Select--",
        label="Location",
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'location', 'name':'location'})
    )
    STATUS_LIST = ((1, 'Active'),(0, 'Inactive'))
    status = forms.ChoiceField(
        label="Status",
        choices=STATUS_LIST,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'status', 'name':'status'})
    )
    serial_number = forms.CharField(
        label="Serial Number",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'serial_number', 'name':'serial_number'})
    )
    os = forms.CharField(
        label="Firmware",
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'os', 'name':'os'})
    )
    tagline = forms.CharField(
        label="Tagline",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'tagline', 'name':'tagline', 'rows':2})
    )
    input_date = forms.DateTimeField(
        label="Date Added",
        widget=forms.DateInput(format='%m/%d/%Y',attrs={'class': 'form-control', 'id' : 'datepicker', 'name':'input_date'})
    )
