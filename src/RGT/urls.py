from django.conf.urls import include, url
from django.contrib import admin
from authentication.views.RegistrationView import RegistrationView
from authentication.views.LoginView import LoginView
from authentication.views.LogoutRedirectView import LogoutRedirectView
from authentication.views.ForgotPasswordView import ForgotPasswordView
from authentication.views.ChangePasswordView import ChangePasswordView
from . import authentication
from . import userProfile
from . import contact
from . import views

admin.autodiscover()

urlpatterns = [
               url(r'^admin/', include(admin.site.urls)),
               url(r'^$', views.home),
               url(r'^home/', views.home),
               url(r'^auth/register/', RegistrationView.as_view()),
               url(r'^auth/login/', LoginView.as_view()),
               url(r'^auth/logout/', LogoutRedirectView.as_view()),
               url(r'^accounts/login/', LoginView.as_view()),
               url(r'^auth/verify/(?P<verifyEmailCode>[A-Za-z0-9]+)/$',
                   authentication.registration.views.verify),
               url(r'^accounts/forgot/$', ForgotPasswordView.as_view()),
               url(r'^accounts/recover/$', authentication.recoverPassword.views.recoverPass),
               url(r'^accounts/recover/(?P<passRecoverCode>[A-Za-z0-9]+)/$',
                   authentication.recoverPassword.views.recoverPass),
               url(r'^accounts/change/', ChangePasswordView.as_view()),
               url(r'^profile/$', userProfile.views.displayUserProfile),
               url(r'^profile/displayHelp$', userProfile.views.ajaxGetDisplayHelpState),
               url(r'^contact/', contact.views.contact),
               url(r'^grids/', include('RGT.gridMng.urls')),
               # url(r'^grids/', gridMng.urls),
               url(r'^sessions/', include('RGT.gridMng.session.urls')),
               url(r'^help/(?P<helpMessageId>.*)/$', views.rgtHelp)]
