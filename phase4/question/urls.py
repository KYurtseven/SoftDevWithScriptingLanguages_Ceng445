from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/$', views.add, name = "add"),
    # /question only
    url(r'^(?P<q_id>[\w\-]+)/$', views.index, name = 'index'),
    url(r'^edit/(?P<q_id>[\w\-]+)/$', views.edit , name = 'edit'),
    url(r'^getquestion$', views.getquestion, name='Get current question'),

    url(r'^updbody$', views.updbody, name='update question body'),
    url(r'^upddate$', views.upddate, name='update question date'),
    url(r'^updparent$', views.updparent, name='update question parent'),
    
    url(r'^addtopic$', views.addtopic, name='add question topic'),
    url(r'^topiclist$', views.topiclist, name='returns topic list'),
    url(r'^updtopic$', views.updtopic, name='update question topic'),
    url(r'^deltopic/(?P<q_id>[\w\-]+)/(?P<t_id>[0-9]+)$', views.deltopic, name="delete question topic"),
    
    url(r'^addembed$', views.addembed, name='add question embed'),
    url(r'^embedlist$', views.embedlist, name='returns embed list'),
    url(r'^updembed$', views.updembed, name='update question embed'),
    url(r'^delembed/(?P<q_id>[\w\-]+)/(?P<e_id>[0-9]+)$', views.delembed, name="delete question embed"),

    url(r'^addchoice$', views.addchoice, name='add question choice'),
    url(r'^choicelist$', views.choicelist, name='returns choice list'),
    url(r'^updchoice$', views.updchoice, name='update question choice'),
    url(r'^delchoice/(?P<q_id>[\w\-]+)/(?P<c_id>[0-9]+)$', views.delchoice, name="delete question choice"),

    url(r'^getpdf/(?P<q_id>[\w\-]+)/$', views.getpdf, name= "Question pdf"),
];



