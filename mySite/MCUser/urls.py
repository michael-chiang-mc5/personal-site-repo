from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user_profile/(?P<user_pk>[0-9]+)/$', views.user_profile, name='user_profile'),
]
