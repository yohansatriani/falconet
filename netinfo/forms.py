from django import forms

class SiteForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'id', 'name':'id'})
    )
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'name', 'name':'name'})
    )
    type = forms.CharField(
        label="Type",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'type', 'name':'type'})
    )
    location = forms.CharField(
        label="Location",
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'location', 'name':'location', 'rows':3})
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'city', 'name':'city'})
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
    CONTACT_TYPE = (('phone', 'PHONE'),('fax', 'FAX'),)
    contact_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'contact_id', 'name':'contact_id[]'})
    )
    # site_id = forms.IntegerField(
    #     label="Site",
    #     widget=forms.HiddenInput(attrs={'class': 'form-control', 'id' : 'site_id', 'name':'site_id[]'})
    # )
    contact_type = forms.ChoiceField(
        label="Type",
        choices=CONTACT_TYPE,
        widget=forms.Select(attrs={'class': 'col-sm-3 form-control', 'id' : 'contact_type', 'name':'contact_type[]'})
    )
    contact_number = forms.CharField(
        label="Number",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'contact_number', 'name':'contact_number[]'})
    )

