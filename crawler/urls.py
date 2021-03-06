#-*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.page_header, name='page_header'),
    url(r'^crawler/$', views.crawler, name='crawler'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^signup_ok/$', views.sign_up_ok, name='sign_up_ok'),
    url(r'^addsite/$', views.add_site, name='add_site'),
    url(r'^addrequest/$', views.add_request, name='add_request'),
    url(r'^ajax/data/$', views.ajax_data, name='ajax_data'),
    url(r'^ajax/data_final/$', views.add_complete, name='add_complete'),
]