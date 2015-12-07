from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /papers/
    url(r'^$', views.index, name='index'),
]
