from django import forms
from datetime import timedelta
import datetime
from django.utils import timezone
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget
from django.core import validators
from .models import *
from django.forms.models import ModelChoiceField
from django.forms import ModelForm, CharField

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
	('one', "Last Hour"),
	('three', "Last 3 Hours"),
	('six', "Last 6 Hours"),
	('twelve', "Last 12 Hours"),
	('twentyfour', "Last 24 Hours"),
	('week', "Last Week"),
	('month', "Last Month"),
	('custom', "Custom Selection"),

)

class TrafficReport (forms.Form):

	traffic_type = forms.ChoiceField(choices=TRAFFIC_CHOICES)
	checkbox   = forms.BooleanField(required=False, widget=forms.CheckboxInput( attrs = {'onclick' : 'showHide();'}))
	address    = forms.CharField(required=False, validators=[validators.validate_ipv4_address],
								widget=forms.TextInput(attrs={'placeholder': 'IP Address'})	)
	time_range = forms.ChoiceField(required=False, choices = TIME_PERIOD, widget=forms.Select(attrs = 
									{'onchange' : 'showHideTime();'}))
	start_date = forms.DateField(widget=SelectDateWidget)
	end_date   = forms.DateField(widget=SelectDateWidget, initial=timezone.now())

	def clean(self):
		cleaned_data = super(TrafficReport, self).clean()
		checkbox = cleaned_data.get('checkbox')
		address  = cleaned_data.get('address')
		if not checkbox  and  not address:
			self.add_error('address', '(Select either all IP addresses or input one IP)')


class CustomReport (forms.Form):


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


	def clean(self):
		cleaned_data = super(CustomReport, self).clean()
		dst_addr = cleaned_data.get("dst_addr")
		src_addr = cleaned_data.get("src_addr")
		traffic_type = cleaned_data.get('traffic_type')
		if dst_addr and traffic_type == 'Outgoing':
			self.add_error('traffic_type', '(Outgoing traffic has only source address)')
		elif src_addr and traffic_type == "Incoming":
			self.add_error('traffic_type', '(Incoming traffic has only destination address)')

class SelectDeviceForm(forms.Form):  
	device_name = forms.ChoiceField()

	def __init__(self, *args, **kwargs):
		super(forms.Form, self).__init__(*args, **kwargs)
		self.fields['device_name'].choices = [(l.device_ip, l.device_name) for l in Devices.objects.all()]


#service classes
from django.forms import ModelChoiceField
class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.rate_name

class DeviceNameChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.device_name
####


class AddDeviceForm(ModelForm):
    device_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'required': "true"}))
    device_ip =  forms.CharField(validators=[validators.validate_ipv4_address], widget=forms.TextInput(attrs={'placeholder': 'IP Address', 'required': "true"}))
    billing = MyModelChoiceField(queryset = Billing.objects.all(), empty_label=None)

    class Meta:
        model = Devices
        fields = ['device_name', 'device_ip', 'billing']

class RemoveDeviceForm(ModelForm):
    device_name = DeviceNameChoiceField(queryset=Devices.objects.all(), empty_label=None)
    checkbox   = forms.BooleanField(required=False, widget=forms.CheckboxInput)
    class Meta:
        model = Devices
        fields = ['device_name']

class ChangeDeviceBillingForm(ModelForm):
    device_name = DeviceNameChoiceField(queryset=Devices.objects.all(), empty_label=None)
    billing = MyModelChoiceField(queryset = Billing.objects.all(), empty_label=None)

    class Meta:
        model = Devices
        fields = ['device_name', 'billing']

class AddBillingForm(ModelForm):

    STATE_CHOICES = (
        (1, 'Yes'),
        (0, 'No'),
    )

    rate_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 1GB=0.02$', 'required': "true"}))
    billable = forms.ChoiceField(choices= STATE_CHOICES)
    cost_rate = forms.FloatField(required = False, widget=forms.TextInput(attrs={'placeholder': 'e.g. 0.05', 
                                             }),validators=[validators.RegexValidator(regex='^[0-9,.]*$',
                                             message='Use point to separate float numbers',code='invalid_number')])

    class Meta:
        model = Billing
        fields=['rate_name', 'billable', 'cost_rate']

class RemoveBillingForm(ModelForm):
    rate_name= MyModelChoiceField(queryset = Billing.objects.all(), empty_label=None)

    class Meta:
        model = Billing
        fields = ['rate_name']


class CalculateBillingForm(SelectDeviceForm):

	traffic_type = forms.ChoiceField(choices=TRAFFIC_CHOICES)
	checkbox   = forms.BooleanField(required=False, widget=forms.CheckboxInput( 
													attrs = {'onclick' : 'showHide();'}))
	address    = forms.CharField(required=False, validators=[validators.validate_ipv4_address],
								widget=forms.TextInput(attrs={'placeholder': 'IP Address'})	)
	time_range 		= forms.ChoiceField(required=False, choices = TIME_PERIOD, widget=forms.Select(attrs = 
									{'onchange' : 'showHideTime();'}))
	start_date		= forms.DateField(widget=SelectDateWidget)
	end_date   		= forms.DateField(widget=SelectDateWidget, initial=timezone.now())
	
	def clean(self):
		cleaned_data = super(CalculateBillingForm, self).clean()
		checkbox = cleaned_data.get('checkbox')
		address  = cleaned_data.get('address')
		if not checkbox  and  not address:
			self.add_error('address', '(Select either all IP addresses or input one IP)')

