from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.top_conversations_app, name='top_conversations'),

]