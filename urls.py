from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CSM.views.home', name='home'),
    # url(r'^CSM/', include('CSM.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Authentication
    (r'^owners/login/$', 'django.contrib.auth.views.login'),
    (r'^owners/changepassword/$', 'django.contrib.auth.views.password_change'),
    (r'^owners/changepassworddone/$', 'django.contrib.auth.views.password_change_done'),
    (r'^owners/resetpassword/$', 'django.contrib.auth.views.password_reset'),
    (r'^owners/resetpassworddone/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^owners/resetpasswordconfirm/$', 'django.contrib.auth.views.password_reset_confirm'),

    # Owners
    (r'^owners/home/$', 'csm.views.editowner'),
    (r'^owners/(?P<ownerid>\d+)/edit/$', 'csm.views.editowner'),
    (r'^owners/add/$', 'csm.views.editowner'),
    (r'^owners/addindividual/$', 'csm.views.addindividual'),
)
