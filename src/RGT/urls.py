from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from authentication.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'RGT.views.home'),
    #url(r'^$', 'RGT.applicationForm.views.showAppForm'),
    #url(r'^registerCloseBeta/$', 'RGT.applicationForm.views.registerUser'),
    #url(r'^thx/$', 'RGT.applicationForm.views.showThankYouPage'),
    url(r'^home/', 'RGT.views.home'),
    url(r'^auth/register/', RegistrationView.as_view()),
    url(r'^auth/login/', LoginView.as_view()),
    url(r'^auth/logout/', LogoutRedirectView.as_view()),
    url(r'^auth/verify/(?P<verifyEmailCode>[A-Za-z0-9]+)/$', 'RGT.authentication.registration.views.verify'),
    url(r'^accounts/forgot/$', ForgotPasswordView.as_view()),
    url(r'^accounts/recover/$', 'RGT.authentication.recoverPassword.views.recoverPass'),
    url(r'^accounts/recover/(?P<passRecoverCode>[A-Za-z0-9]+)/$', 'RGT.authentication.recoverPassword.views.recoverPass'),
    url(r'^accounts/change/', ChangePasswordView.as_view()),
    url(r'^profile/$', 'RGT.userProfile.views.displayUserProfile'),
    url(r'^profile/displayHelp$', 'RGT.userProfile.views.ajaxGetDisplayHelpState'),
    url(r'^contact/', 'RGT.contact.views.contact'),
    url(r'^grids/', include('RGT.gridMng.urls')),
    url(r'^sessions/', include('RGT.gridMng.session.urls')),
)
