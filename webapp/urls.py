from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
import studywizard.views as views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'home.html'}, name='home'),
    url(r'^dropbox/auth/$', views.dropbox_auth),
    url(r'^dropbox/auth/result/$', views.post_dropbox_auth),
    url(r'^dropbox/auth/failed/$', direct_to_template, {'template': 'failed_dropbox_auth.html'}, name='failed_dropbox_auth'),
    url(r'^apps/$', views.app_list),
    url(r'^create/$', views.app_create),
    url(r'^thanks/$', views.app_thanks),
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^webapp/', include('webapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
