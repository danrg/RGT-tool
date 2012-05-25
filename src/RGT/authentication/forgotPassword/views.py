from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import redirect_to
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from forgotPassForm import ForgotPassForm
from RGT.gridMng import utility
from RGT.authentication.models import PassRecoverCode
from RGT.utils import sendMail
from recaptcha.client import captcha

def forgotPass(request):
    if request.user.is_authenticated():
        return redirect_to(request, '/home/')
    
    if request.method == 'POST':
        form = ForgotPassForm(request.POST)
        form.full_clean()
        #re_captcha response from the POST request that we sent to their service
        response = captcha.submit(  
            request.POST['recaptcha_challenge_field'],  
            request.POST['recaptcha_response_field'],  
            'USE_YOUR_OWN',  #private key
            request.META['REMOTE_ADDR'],)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            if response.is_valid:
                # send the email for the new password request
                subject = 'New password request for RGT!'
                toMail = form.cleaned_data['email']
                htmlContentTemplate = 'authentication/forgotPassEmail.html'
                linkInitialPart = settings.HOST_NAME+'/accounts/recover/'
                generatedCode = utility.randomStringGenerator(14)
                textContent = 'Click this link to change your password.'
                fromMail = settings.EMAIL_HOST_USER
                if sendMail(subject, toMail, fromMail, htmlContentTemplate, linkInitialPart,
                            generatedCode, user, textContent):
                    code = PassRecoverCode()
                    code.email = toMail
                    code.linkCode = generatedCode
                    code.save()
                    request.session['checkEmail'] = True
                    return HttpResponseRedirect('/accounts/forgot/')
                else:
                    # error in sending mail
                    pass
            else:
                # error in re_captcha
                pass
        else:
            # form has errors
            pass
        
        return render_to_response('authentication/forgotPass.html', 
                      {'form': form}, context_instance=RequestContext(request))
    else:
        # GET request
        form = ForgotPassForm()
        checkEmail = request.session.get('checkEmail')
        if checkEmail != None:
            del request.session['checkEmail']
        
    return render_to_response('authentication/forgotPass.html', 
                              {'form': form, 'checkEmail': checkEmail}, context_instance=RequestContext(request))
        
        
    