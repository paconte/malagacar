from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rent$', views.index, name='rent'),
    url(r'^booking$', views.booking, name='booking'),
]
