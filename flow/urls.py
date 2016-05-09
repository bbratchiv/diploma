from django.conf.urls import include, url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.home),
	url(r'^top_incoming/(?P<pk>\d+)/$', views.top_incoming),
	url(r'^top_outgoing/(?P<pk>\d+)/$', views.top_outgoing),
	url(r'^traffic/$', views.traffic_all),
	url(r'^accounts/login/$', auth_views.login),
	url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}),
	url(r'^traffic_report/$', views.traffic_report),
	url(r'^custom_report/$', views.custom_report),
	url(r'^billing/$', views.billing),
	url(r'^home/$', views.home)

]