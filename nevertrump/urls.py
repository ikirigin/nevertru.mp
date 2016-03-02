from django.conf.urls import include, url
from django.contrib import admin

import base.views as baseviews

urlpatterns = [
    # Examples:
    url(r'^$', baseviews.home, name='home'),
    url(r'^pledge$', baseviews.pledge, name='pledge'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
]
