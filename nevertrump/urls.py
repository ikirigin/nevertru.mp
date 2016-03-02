from django.conf.urls import include, url
from django.contrib import admin

import base.views as baseviews

urlpatterns = [
    # Examples:
    url(r'^$', baseviews.home, name='home'),
    url(r'^pledge$', baseviews.makepledge, name='makepledge'),
    url(r'^verify', baseviews.verify, name='verify'),
    
    url(r'^reflect_user', baseviews.reflect_user, name='reflect_user'),
    url(r'^logout', baseviews.logoutview, name='logout'),
    
    
    # MUST BE LAST!
    url(r'^(?P<code>\w+)$', baseviews.verifypledge, name='verifypledge'),
]
