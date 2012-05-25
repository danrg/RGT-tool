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

def register(request):
    if request.user.is_authenticated():
        return redirect_to(request, '/home/')
    
    if request.method == 'POST':
        registrationForm = RegistrationForm(request.POST)
        #registrationForm.full_clean()
        #re_captcha response from the POST request that we sent to their service
        response = captcha.submit(  
            request.POST['recaptcha_challenge_field'],  
            request.POST['recaptcha_response_field'],  
            'USE_YOUR_OWN',  #private key
            request.META['REMOTE_ADDR'],)
        if registrationForm.is_valid():
            # check if re_captcha is valid 
            if response.is_valid:
                user = User.objects.create_user(registrationForm.cleaned_data['email'], registrationForm.cleaned_data['email'], registrationForm.cleaned_data['password']);
                user.first_name = registrationForm.cleaned_data['firstName']
                user.last_name = registrationForm.cleaned_data['lastName']
                user.save();
                
                #login the user after creation
                user = authenticate(email= registrationForm.cleaned_data['email'], password= registrationForm.cleaned_data['password'])
                login(request, user);
                
                # send email verification email
                subject = 'Email verification for RGT!'
                toMail = registrationForm.cleaned_data['email']
                htmlContentTemplate = 'authentication/verifyEmail.html'
                linkInitialPart = settings.HOST_NAME+'/auth/verify/'
                code = utility.randomStringGenerator(14)
                textContent = 'Click this link to verify your email.'
                fromMail = settings.EMAIL_HOST_USER
                if sendMail(subject, toMail, fromMail, htmlContentTemplate, linkInitialPart,
                            code, user, textContent):
                    profile = user.get_profile()
                    profile.verifyEmailCode = code
                    profile.save();
                    return HttpResponseRedirect('/home/');
                else:
                    # problem with email sending
                    pass
            else:
                # error in re_captcha
                pass
        else:
            # errors in form
            pass
        
        return render_to_response('authentication/register.html', 
                      {'form': registrationForm},
                      context_instance=RequestContext(request))
    else:
        form= RegistrationForm()

    return render_to_response('authentication/register.html',
                              {'form': form},
                              context_instance=RequestContext(request))

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
        
        
        
        
        