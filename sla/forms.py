from django import forms
from sla.models import troubles
from netinfo.models import links
from django.forms import ModelChoiceField

class LinksModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.links_name

class TroubleForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'id', 'name':'id'})
    )
    link = LinksModelChoiceField(
        queryset=links.objects.all(),
        empty_label="--Please-Select--",
        label="Link",
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'link', 'name':'link'})
    )
    CAUSE_TYPE = (('ISP', 'ISP'),('INTERNAL', 'INTERNAL'))
    cause_type = forms.ChoiceField(
        label="Cause Type",
        choices=CAUSE_TYPE,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'cause_type', 'name':'cause_type'})
    )
    start_time = forms.DateTimeField(
        label="Start Time",
        widget=forms.DateInput(format='%Y-%m-%d %H:%M',attrs={'class': 'form-control', 'id' : 'start_datetimepicker', 'name':'start_time'})
    )
    end_time = forms.DateTimeField(
        label="End Time",
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d %H:%M',attrs={'class': 'form-control', 'id' : 'end_datetimepicker', 'name':'end_time'})
    )
    status = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'status', 'name':'status'})
    )
    description = forms.CharField(
        label="Description",
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'description', 'name':'description', 'rows':2})
    )
    isp_ticket = forms.CharField(
        label="ISP Ticket Number",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'isp_ticket', 'name':'isp_ticket'})
    )
