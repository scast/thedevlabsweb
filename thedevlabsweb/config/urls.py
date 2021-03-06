# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from thedevlabsweb.recommender.views import (
    TwitterSearchView, URLAddView, URLGetView, URLUpvoteView, URLDownvoteView
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^search/$', TwitterSearchView.as_view(), name='search'),
    url(r'^recommender/discover/$',
        URLGetView.as_view(), name='discover'),
    url(r'^recommender/discover/(?P<id>\d+)/like/$',
        URLUpvoteView.as_view(), name='discover_like'),
    url(r'^recommender/discover/(?P<id>\d+)/dislike/$',
        URLUpvoteView.as_view(), name='discover_dislike'),
    url(r'^recommender/add/$',
        URLAddView.as_view(), name='add_website'),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
    url(r'^avatar/', include('avatar.urls')),

    # Your stuff: custom urls go here

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
