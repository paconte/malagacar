from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^booking/(?P<car_id>\d+)/$', views.booking, name='booking'),
    url(r'^confirmation$', views.booking_confirmation, name='booking_confirmation'),
]
