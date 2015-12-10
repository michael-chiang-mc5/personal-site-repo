from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.frontpage, name='frontpage'),
    url(r'^admin$', views.admin, name='admin'),
    url(r'^list_all$', views.list_all, name='list_all'),
]
