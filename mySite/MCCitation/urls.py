from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /papers/
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<pk>[0-9]+)/(?P<current_thread>[0-9]+)/$', views.detail, name='detail'),
    url(r'^import_from_pubmed/(?P<page>[0-9]+)/$', views.import_from_pubmed, name='import_from_pubmed'),
    url(r'^addCitation/$', views.addCitation, name='addCitation'),
]
