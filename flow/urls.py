from django.conf.urls import include, url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.home, name='home'),
	url(r'^top_incoming/(?P<pk>\d+)/$', views.top_incoming),
	url(r'^top_outgoing/(?P<pk>\d+)/$', views.top_outgoing),
	url(r'^traffic/$', views.traffic_all),
	url(r'^accounts/login/$', auth_views.login),
	url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}),
	url(r'^export/$', views.export_data),
#	url(r'^export/download/$', views.get_xls_data)
]