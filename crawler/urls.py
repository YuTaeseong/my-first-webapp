from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.page_header, name='page_header'),
    url(r'^crawler/(?P<pk>[a-z]+)/$', views.crawler, name='crawler'),
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^signup_ok/$', views.sign_up_ok, name='sign_up_ok'),
    url(r'^addsite/$', views.add_site, name='add_site'),
    url(r'^addrequest/$', views.add_request, name='add_request'),
]