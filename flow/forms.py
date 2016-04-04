from django import forms
from datetime import timedelta
import datetime
from django.utils import timezone
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget
from django.core import validators

TRAFFIC_CHOICES = (
	('Incoming', 'Incoming'),
	('Outgoing', 'Outgoing')
)

CRITERIA_CHOICES = (
#	('null', ''),
	('source_ip', 'Source Address'),
	('dest_ip', 'Destination Address'),
	('port1', 'Port'),
	('port_range', 'Port Range'),
	('protocol', 'Internet Protocol')

)

TIME_PERIOD = (
	('hour', "Last Hour"),
	('3hours', "Last 3 Hours"),
	('6hours', "Last 6 Hours"),
	('12hours', "Last 12 Hours"),
	('24hours', "Last 24 Hours"),
	('week', "Last Week"),
	('month', "Last Month"),
	('custom', "Custom Selection"),

)

class TrafficReport (forms.Form):

	traffic_type = forms.ChoiceField(choices=TRAFFIC_CHOICES)
	checkbox   = forms.BooleanField(required=False, widget=forms.CheckboxInput( attrs = {'onclick' : 'showHide();'}))
	address    = forms.CharField(required=False, validators=[validators.validate_ipv4_address],
								widget=forms.TextInput(attrs={'placeholder': 'IP Address'})	)
	start_date = forms.DateField(widget=SelectDateWidget)
	end_date   = forms.DateField(widget=SelectDateWidget, initial=timezone.now())
	time_range = forms.ChoiceField(required=False, choices = TIME_PERIOD, widget=forms.Select(attrs = 
									{'onchange' : 'showHideTime();'}))
	def clean(self):
		cleaned_data = super(TrafficReport, self).clean()
		checkbox = cleaned_data.get('checkbox')
		address  = cleaned_data.get('address')
		if not checkbox  and  not address:
			self.add_error('address', '(Select either all IP addresses or input one IP)')


class CustomReport (forms.Form):
#	widget=forms.HiddenInput()

	choice_criteria = forms.ChoiceField(choices = CRITERIA_CHOICES, widget=forms.Select(attrs = 
									{'onchange' : 'showHide();'}))
	traffic_type 	= forms.ChoiceField(choices=TRAFFIC_CHOICES)

	src_addr  		= forms.CharField(required=False, validators=[validators.validate_ipv4_address],
								widget=forms.TextInput(attrs={'placeholder': 'Source IP Address', 'class':'cust_rep'}))
	dst_addr  		= forms.CharField(required=False, validators=[validators.validate_ipv4_address],
								widget=forms.TextInput(attrs={'placeholder': 'Destination IP Address', 'class':'cust_rep'}))
	port 			= forms.CharField(required=False, max_length=6, widget=forms.TextInput(attrs={'type':'number', 'class':'cust_rep'}))
	pFrom			= forms.CharField(required=False, max_length=6, widget=forms.TextInput(attrs={'type':'number',
								'placeholder': 'from', 'class':'cust_rep' }))
	pTo				= forms.CharField(required=False, max_length=6, widget=forms.TextInput(attrs={'type':'number',
								'placeholder': 'to', 'class':'cust_rep'}))
	proto 			= forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'e.x. UDP', 'class':'cust_rep'}))
	time_range 		= forms.ChoiceField(required=False, choices = TIME_PERIOD, widget=forms.Select(attrs = 
									{'onchange' : 'showHideTime();'}))
	start_date		= forms.DateField(widget=SelectDateWidget)
	end_date   		= forms.DateField(widget=SelectDateWidget, initial=timezone.now())
