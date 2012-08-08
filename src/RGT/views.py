from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from HelpMessages import HELP_MESSAGES
#import logging
from RGT.gridMng.utility import createXmlSuccessResponse, createXmlErrorResponse

@login_required
def home(request):
    profile = request.user.get_profile()
    return render(request, 'home.html', {'firstName': request.user.first_name, 'verifiedEmail': profile.verifiedEmail})


@login_required
def rgtHelp(request, helpMessageId = ''):
    if helpMessageId in HELP_MESSAGES:
        return HttpResponse(createXmlSuccessResponse(HELP_MESSAGES[helpMessageId]), content_type='application/xml')

    return HttpResponse(createXmlErrorResponse('Help topic not found'), content_type='application/xml')