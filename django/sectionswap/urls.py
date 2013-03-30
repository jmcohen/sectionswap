from django.conf.urls import patterns, include, url
import swap

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'swap.views.index'),
	url(r'^courses$', 'swap.views.courses'),
	url(r'^swaprequest$', 'swap.views.swapRequest'),
	url(r'^login$', 'swap.views.login'),

    # Examples:
    # url(r'^$', 'sectionswap.views.home', name='home'),
    # url(r'^sectionswap/', include('sectionswap.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
