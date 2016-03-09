from django import forms
from datetime import timedelta
import datetime
from django.utils import timezone
from django.forms.extras.widgets import SelectDateWidget
from django.core import validators

TRAFFIC_CHOICES = (
	('Incoming', 'Incoming'),
	('Outgoing', 'Outgoing')
)

class ShowDataForm (forms.Form):

	choice= forms.ChoiceField(choices=TRAFFIC_CHOICES)
	checkbox   = forms.BooleanField(required=False, widget=forms.CheckboxInput( attrs = {'onclick' : 'showHide();'}))
	address    = forms.CharField(required=False, validators=[validators.validate_ipv4_address])
	start_date = forms.DateField(widget=SelectDateWidget)
	end_date   = forms.DateField(widget=SelectDateWidget, initial=timezone.now())
	
	def clean(self):
		cleaned_data = super(ShowDataForm, self).clean()
		checkbox = cleaned_data.get('checkbox')
		address  = cleaned_data.get('address')
		if not checkbox  and  not address:
			self.add_error('address', '(Select either all IP addresses or input one IP)')