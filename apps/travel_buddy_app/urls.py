from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.add),
    url(r'^process$', views.process),
    url(r'^join/(?P<id>\w*)$', views.join),
    url(r'^trip/(?P<id>\w*)$', views.trip),
]
