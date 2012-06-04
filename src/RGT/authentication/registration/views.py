from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic.simple import redirect_to
from django.conf import settings
from registrationForm import RegistrationForm
from RGT.gridMng import utility
from RGT.userProfile.models import UserProfile
from recaptcha.client import captcha
from RGT.utils import sendMail


def verify(request, verifyEmailCode=''):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
        
    if request.method == 'GET':
        if not request.user.is_superuser:
            try:
                profile = UserProfile.objects.get(verifyEmailCode=verifyEmailCode)
                if request.user.id == profile.user_id:
                    if not profile.verifiedEmail:
                        profile.verifiedEmail = True
                        profile.save()
                else:
                    # it is not the same user as the one logged in
                    pass
            except UserProfile.DoesNotExist:
                # a profile with this verify email code does not exist
                pass
        
        return redirect_to(request, '/home/')
