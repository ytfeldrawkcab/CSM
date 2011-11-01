from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import user_passes_test

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

staff_required = user_passes_test(lambda u: u.is_staff)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CSM.views.home', name='home'),
    # url(r'^CSM/', include('CSM.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Static Pages
    
    (r'^owners/$', staff_required(direct_to_template), {'template': 'index.html'}),
    
    # Authentication
    (r'^owners/login/$', 'django.contrib.auth.views.login'),
    (r'^owners/logout/$', 'django.contrib.auth.views.logout'),
    (r'^owners/changepassword/$', 'django.contrib.auth.views.password_change'),
    (r'^owners/changepassworddone/$', 'django.contrib.auth.views.password_change_done'),
    (r'^owners/resetpassword/$', 'django.contrib.auth.views.password_reset', {'is_admin_site':False}),
    (r'^owners/resetpassworddone/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^owners/resetpasswordcomplete/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^owners/resetpasswordconfirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),

    # Owners
    (r'^owners/home/$', 'csm.views.selecthome'),
    (r'^owners/(?P<ownerid>\d+)/edit/$', 'csm.views.editowner'),
    (r'^owners/add/$', 'csm.views.editowner'),
    (r'^owners/addindividual/$', 'csm.views.addindividual'),
    (r'^owners/search/$', 'csm.views.ownersearch'),
)
