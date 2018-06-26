from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^quotes$', views.quotes),
    url(r'^like$', views.like),
    url(r'^delete$', views.delete),
    url(r'^add$', views.add),
    url(r'^logout$', views.logout),
    url(r'^user/(?P<id>\d+)$', views.show),
    url(r'^myaccount/(?P<id>\d+)$', views.edit),
    url(r'^myaccount/update/(?P<id>\d+)$', views.update),
]  