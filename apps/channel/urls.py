"""araplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
# from django.contrib import admin

urlpatterns = [
    url(r'^$', 'apps.channel.views.main'),
    url(r'^post/$', 'apps.channel.views.post_write'),
    url(r'^([^/]+)/$', 'apps.channel.views.post_list'),
    url(r'^([^/]+)/([1-9][0-9]*)/$', 'apps.channel.views.post_read'),
    url(r'^([^/]+)/([1-9][0-9]*)/modify/$', 'apps.channel.views.post_modify'),
    url(r'^([^/]+)/([1-9][0-9]*)/comment/$', 'apps.channel.views.comment'),
    url(r'^([^/]+)/([1-9][0-9]*)/comment_modify/$',
        'apps.channel.views.comment_modify'),
    url(r'^up/$', 'apps.channel.views.up'),
    url(r'^down/$', 'apps.channel.views.down'),
    url(r'^delete/$', 'apps.channel.views.delete'),
    url(r'^report/$', 'apps.channel.views.report'),
]
