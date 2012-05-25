from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic.simple import redirect_to
from changePassForm import ChangePassForm

def changePass(request):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
    
    if request.method == 'POST':
        user = request.user
        form = ChangePassForm(request.POST, request=request)
        form.full_clean()
        if form.is_valid():
            user.set_password(form.cleaned_data['newPassword'])
            user.save()
            request.session['passUpdated'] = True
            return HttpResponseRedirect('/accounts/change/')
        else:
            # form contains errors
            return render_to_response('authentication/changePass.html', 
                                  {'form': form},
                                  context_instance=RequestContext(request))
    else:
        passUpdated = request.session.get('passUpdated')
        if passUpdated != None:
            del request.session['passUpdated']
        form = ChangePassForm()
        return render_to_response('authentication/changePass.html', 
                                  {'form': form, 'passUpdated': passUpdated},
                                  context_instance=RequestContext(request))
        