from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import SetPasswordForm
import settings

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
    (r'^{}login/$'.format(settings.SUBSITE_URL),'django.contrib.auth.views.login'),
    (r'^{}logout/$'.format(settings.SUBSITE_URL), 'django.contrib.auth.views.logout'),
    (r'^{}changepassword/$'.format(settings.SUBSITE_URL), 'django.contrib.auth.views.password_change'),
    (r'^{}changepassworddone/$'.format(settings.SUBSITE_URL), 'django.contrib.auth.views.password_change_done'),
    (r'^{}resetpassword/$'.format(settings.SUBSITE_URL), 'django.contrib.auth.views.password_reset', {'is_admin_site':False}),
    (r'^{}resetpassworddone/$'.format(settings.SUBSITE_URL), 'django.contrib.auth.views.password_reset_done'),
    (r'^{}resetpasswordcomplete/$'.format(settings.SUBSITE_URL), 'django.contrib.auth.views.password_reset_complete'),
    (r'^{}resetpasswordconfirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$'.format(settings.SUBSITE_URL), 'django.contrib.auth.views.password_reset_confirm'),

    # Owners
    (r'^{}$'.format(settings.SUBSITE_URL), 'csm.views.selecthome'),
    (r'^{}(?P<ownerid>\d+)/edit/$'.format(settings.SUBSITE_URL), 'csm.views.editowner'),
    (r'^{}add/$'.format(settings.SUBSITE_URL), 'csm.views.editowner'),
    (r'^{}addindividual/$'.format(settings.SUBSITE_URL), 'csm.views.addindividual'),
    (r'^{}search/$'.format(settings.SUBSITE_URL), 'csm.views.ownersearch'),
    
    # Elections
    (r'^{}elections/(?P<electionid>\d+)/$'.format(settings.SUBSITE_URL), 'csm.views.selectelection'),
    (r'^{}elections/add/$'.format(settings.SUBSITE_URL), 'csm.views.editelection'),
    (r'^{}elections/addcandidate/$'.format(settings.SUBSITE_URL), 'csm.views.addcandidate'),
    (r'^{}elections/search/$'.format(settings.SUBSITE_URL), 'csm.views.electionsearch'),
    
    # Users
    (r'^{}users/(?P<userid>\d+)/edit/$'.format(settings.SUBSITE_URL), 'csm.views.edituser'),
    (r'^{}users/add/$'.format(settings.SUBSITE_URL), 'csm.views.edituser'),
    (r'^{}users/search/$'.format(settings.SUBSITE_URL), 'csm.views.usersearch'),
)
