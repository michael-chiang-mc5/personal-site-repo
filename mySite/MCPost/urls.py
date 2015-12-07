from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /papers/
    url(r'^$', views.index, name='index'),
    url(r'^createPost/$', views.createPost, name='createPost'),
    url(r'^editPost/$', views.editPost, name='editPost'),
    url(r'^replyPost/$', views.replyPost, name='replyPost'),    
]
