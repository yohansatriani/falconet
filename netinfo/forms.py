from django import forms

class SiteForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'name', 'name':'name'}))
    type = forms.CharField(label="Type", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'type', 'name':'type'}))
    location = forms.CharField(label="Location", max_length=300, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'location', 'name':'location', 'rows':3}))
    city = forms.CharField(label="City", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'city', 'name':'city'}))
    description = forms.CharField(label="Description", max_length=100, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'description', 'name':'description', 'rows':2}))
    ipadd = forms.GenericIPAddressField(label="IP Address", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'ipadd', 'name':'ipadd'}))
    site_code = forms.CharField(label="Site code", max_length=3, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'site_code', 'name':'site_code'}))
    area_code = forms.CharField(label="Area code", max_length=3, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'area_code', 'name':'area_code'}))
    tagline = forms.CharField(label="Tagline", max_length=500, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'tagline', 'name':'tagline', 'rows':2}))