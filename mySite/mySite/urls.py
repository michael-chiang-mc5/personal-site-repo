"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.MCHome, name='MCHome')
Class-based views
    1. Add an import:  from other_app.views import MCHome
    2. Add a URL to urlpatterns:  url(r'^$', MCHome.as_view(), name='MCHome')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')), # for description, see: https://docs.djangoproject.com/en/1.8/topics/auth/default/#using-the-views for description of django.contrib.auth.urls
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('MCHome.urls', namespace='MCHome')),
    url(r'^MCUser/', include('MCUser.urls', namespace='MCUser')),
    url(r'^MCPost/', include('MCPost.urls', namespace='MCPost')),
    url(r'^MCCitation/', include('MCCitation.urls', namespace='MCCitation')),
    url(r'^MCDiscussCitation/', include('MCDiscussCitation.urls', namespace='MCDiscussCitation')),
]
