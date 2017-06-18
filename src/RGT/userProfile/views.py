from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
# from RGT.userProfile.userProfileForm import UserProfileForm
from .userProfileForm import UserProfileForm
# from .response.xml.htmlResponseUtil import createXmlSuccessResponse, createXmlErrorResponse
# from ..gridMng.response.xml.htmlResponseUtil import createXmlSuccessResponse, createXmlErrorResponse


def ajaxGetDisplayHelpState(request):
    if not request.user.is_authenticated():
        return HttpResponse(createXmlErrorResponse('You are not logged in, please log in.'),
                            content_type='application/xml')

    profile = request.user.profile

    from ..gridMng.response.xml.htmlResponseUtil import createXmlSuccessResponse
    return HttpResponse(createXmlSuccessResponse(`profile.displayHelp`), content_type='application/xml')


def displayUserProfile(request):
    if not request.user.is_authenticated():
        return redirect('/auth/login/')

    # post = save stuff else just display
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = user.profile
            profile.address = form.cleaned_data['address']
            profile.phone = form.cleaned_data['phone']
            profile.displayHelp = form.cleaned_data['displayHelp']
            profile.save()
            user.first_name = form.cleaned_data['firstName']
            user.last_name = form.cleaned_data['lastName']
            user.save()
            request.session['profileUpdated'] = True
            return HttpResponseRedirect('/profile/')
        else:
            # form contains errors
            return render('userProfile/userProfile.html',
                          {'form': form},
                          context_instance=RequestContext(request))
    else:
        profileUpdated = request.session.get('profileUpdated')
        if 'profileUpdated' in request.session:
            del request.session['profileUpdated']
        profile = user.profile
        form = UserProfileForm(initial={'firstName': user.first_name,
                                        'lastName': user.last_name,
                                        'address': profile.address,
                                        'phone': profile.phone,
                                        'displayHelp': profile.displayHelp,
                                        })
        return render(request,
                      'userProfile/userProfile.html')

