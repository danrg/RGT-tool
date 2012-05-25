from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RGT.views.home', name='home'),
    # url(r'^RGT/', include('RGT.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'RGT.views.home'),
    #url(r'^$', 'RGT.applicationForm.views.showAppForm'),
    #url(r'^registerCloseBeta/$', 'RGT.applicationForm.views.registerUser'),
    #url(r'^thx/$', 'RGT.applicationForm.views.showThankYouPage'),
    url(r'^home/', 'RGT.views.home'),
    url(r'^auth/register/', 'RGT.authentication.registration.views.register'),
    url(r'^auth/login/', 'RGT.authentication.login.views.login'),
    url(r'^auth/logout/', 'RGT.authentication.login.views.logout'),
    url(r'^auth/verify/(?P<verifyEmailCode>[A-Za-z0-9]+)/$', 'RGT.authentication.registration.views.verify'),
    url(r'^accounts/forgot/$', 'RGT.authentication.forgotPassword.views.forgotPass'),
    url(r'^accounts/recover/$', 'RGT.authentication.recoverPassword.views.recoverPass'),
    url(r'^accounts/recover/(?P<passRecoverCode>[A-Za-z0-9]+)/$', 'RGT.authentication.recoverPassword.views.recoverPass'),
    url(r'^accounts/change/', 'RGT.authentication.changePassword.views.changePass'),
    url(r'^profile/', 'RGT.userProfile.views.displayUserProfile'),
    url(r'^contact/', 'RGT.contact.views.contact'),
    url(r'^grids/', include('RGT.gridMng.urls')),
    url(r'^sessions/', include('RGT.gridMng.session.urls')),
)
