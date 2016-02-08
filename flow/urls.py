from django.conf.urls import include, url
from . import views
from django.contrib import admin


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.home, name='home'),
	url(r'^top_incoming/(?P<pk>\d+)/$', views.top_incoming),
	url(r'^top_outgoing/(?P<pk>\d+)/$', views.top_outgoing),
#	url(r'^top_incoming/(?P<pk>[0-9]+])/$', views.top_incoming, name = 'top_incoming'),
#	url(r'^top_outgoing/(?P<pk>[0-9]+])/$', views.top_outgoing, name = 'top_outgoing'),
]