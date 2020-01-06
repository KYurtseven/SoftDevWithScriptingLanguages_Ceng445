from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/$', views.add, name = "add"),
    # /question only
    url(r'^(?P<q_id>[\w\-]+)/$', views.index, name = 'index'),
    # TODO
    # our id could be a string
    url(r'^edit/(?P<q_id>[\w\-]+)/$', views.edit , name = 'edit')
];

