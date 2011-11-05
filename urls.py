from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import SetPasswordForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

staff_required = user_passes_test(lambda u: u.is_staff)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CSM.views.home', name='home'),
    # url(r'^CSM/', include('CSM.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    # Static Pages
    
    # Authentication
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^changepassword/$', 'django.contrib.auth.views.password_change'),
    (r'^changepassworddone/$', 'django.contrib.auth.views.password_change_done'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset', {'is_admin_site':False}),
    (r'^resetpassworddone/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^resetpasswordcomplete/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^resetpasswordconfirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),

    # Owners
    (r'^$', 'csm.views.selecthome'),
    (r'^(?P<ownerid>\d+)/edit/$', 'csm.views.editowner'),
    (r'^add/$', 'csm.views.editowner'),
    (r'^addindividual/$', 'csm.views.addindividual'),
    (r'^search/$', 'csm.views.ownersearch'),
    
    # Elections
    (r'^elections/(?P<electionid>\d+)/$', 'csm.views.selectelection'),
    (r'^elections/add/$', 'csm.views.editelection'),
    (r'^elections/addcandidate/$', 'csm.views.addcandidate'),
    (r'^elections/search/$', 'csm.views.electionsearch'),
    
    # Users
    (r'^users/(?P<userid>\d+)/edit/$', 'csm.views.edituser'),
    (r'^users/add/$', 'csm.views.edituser'),
    (r'^users/search/$', 'csm.views.usersearch'),
)
