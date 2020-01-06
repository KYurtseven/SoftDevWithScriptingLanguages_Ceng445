from django.conf.urls import url
from . import views

urlpatterns = [
    # /question only
    url(r'^$', views.index, name = 'index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^details/(?P<e_id>[\w\-]+)/$', views.details, name = 'details'),
    url(r'^edit/(?P<e_id>[\w\-]+)/$', views.edit, name = 'edit')
];