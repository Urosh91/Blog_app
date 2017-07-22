from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^create/$', views.post_create, name='create'),
    # url(r'^list/$', views.post_list, name='list'),
    url(r'^(?P<pk>\d+)/$', views.comment_thread, name='thread'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.comment_delete, name='delete'),
]
