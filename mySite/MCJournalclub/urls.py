from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^import_from_pubmed/(?P<page>[0-9]+)/$', views.import_from_pubmed, name='import_from_pubmed'),
]
