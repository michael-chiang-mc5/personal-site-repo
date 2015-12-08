from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^detail/(?P<citation_pk>[0-9]+)/(?P<current_thread>[0-9]+)/$', views.detail, name='detail'),
]
