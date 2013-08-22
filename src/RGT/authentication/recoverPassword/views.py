from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
#from django.views.generic.simple import redirect_to
import datetime
from django.utils.timezone import utc
from recoverPassForm import RecoverPassForm
from RGT.authentication.models import PassRecoverCode

def recoverPass(request, passRecoverCode=''):
    if request.user.is_authenticated():
        return redirect('/home/')
    
    if request.method == 'POST':
        postLinkCode = request.POST['linkCode']
        form = RecoverPassForm(request.POST)
        form.full_clean()
        try:
            code = PassRecoverCode.objects.get(linkCode=postLinkCode)
            if code.linkUsed == False and code.linkExpired == False:
                invalidLink = False
                if form.is_valid():
                    try:
                        user = User.objects.get(email=code.email)
                        user.set_password(form.cleaned_data['password'])
                        user.save()
                        code.linkUsed = True
                        code.save()
                        user = authenticate(email=code.email, password=form.cleaned_data['password'])
                        login(request, user)
                        return HttpResponseRedirect('/home/')
                    except User.DoesNotExist:
                        # i do not know if we need that here
                        # user does not exist
                        pass
                else:
                    # form has errors
                    return render_to_response('authentication/recoverPassword.html', 
                                      {'form': form, 'invalidLink': invalidLink, 'linkCode': code.linkCode},
                                      context_instance=RequestContext(request))
            else:
                # code has been used
                invalidLink = True
        except PassRecoverCode.DoesNotExist:
            # code does not exist
            invalidLink = True
            
        return render_to_response('authentication/recoverPassword.html', 
                              {'invalidLink': invalidLink},
                              context_instance=RequestContext(request))
    else:
        # GET request
        # check if the link is still active
        try:
            code = PassRecoverCode.objects.get(linkCode=passRecoverCode)
            if code.linkUsed == False:
                # check date time of the code if it has expired
                codeDate = code.dateTime
                now = datetime.datetime.utcnow().replace(tzinfo=utc)
                dateSub = now - codeDate
                if (dateSub.seconds / 60 < 10):
                    form = RecoverPassForm()
                    invalidLink = False
                    return render_to_response('authentication/recoverPassword.html', 
                                  {'form': form, 'invalidLink': invalidLink, 'linkCode': code.linkCode},
                                  context_instance=RequestContext(request))
                else:
                    # probably this should not happen here, we should check the time
                    # somehow different. maybe with a script in the database
                    # code has expired
                    invalidLink = True
                    code.linkExpired = True
                    code.save()
            else:
                # code has been already used
                invalidLink = True
        except PassRecoverCode.DoesNotExist:
            # code does not exist
            invalidLink = True
            
        return render_to_response('authentication/recoverPassword.html', 
                              {'invalidLink': invalidLink},
                              context_instance=RequestContext(request))
        
    