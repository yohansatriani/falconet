from django import forms

class SiteForm(forms.Form):
    name = forms.CharField(label="name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'name', 'name':'name'}))
    type = forms.CharField(label="type", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'type', 'name':'type'}))
    ipadd = forms.GenericIPAddressField(label="ipadd", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'ipadd', 'name':'ipadd'}))
    site_code = forms.CharField(label="site_code", max_length=3, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'site_code', 'name':'site_code'}))
    area_code = forms.CharField(label="area_code", max_length=3, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'area_code', 'name':'area_code'}))
    location = forms.CharField(label="location", max_length=300, widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'location', 'name':'location', 'rows':3}))
    city = forms.CharField(label="city", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'type' :'text', 'id' : 'city', 'name':'city'}))
    tagline = forms.CharField(label="tagline", max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'tagline', 'name':'tagline', 'rows':2}))
    description = forms.CharField(label="description", max_length=100, widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'description', 'name':'description', 'rows':2}))