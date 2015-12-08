from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^createPost/$', views.createPost, name='createPost'),
    url(r'^editPost/$', views.editPost, name='editPost'),
    url(r'^replyPost/$', views.replyPost, name='replyPost'),
    url(r'^post_editor/$', views.post_editor, name='post_editor'),
    url(r'^deletePost/$', views.deletePost, name='deletePost'),
    url(r'^post_context/(?P<post_pk>[0-9]+)/$', views.post_context, name='post_context'),
]
