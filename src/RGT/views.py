from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.simple import redirect_to
from HelpMessages import HELP_MESSAGES
#import logging
from RGT.gridMng.utility import createXmlSuccessResponse, createXmlErrorResponse

def home(request):
    if request.user.is_authenticated():
        # Get an instance of the logger
        #logger = logging.getLogger('django')
        # Log a message at a debug level
        #logger.warning('user is on home page')
        profile = request.user.get_profile()
        return render(request, 'home.html',
                      {'firstName': request.user.first_name, 'verifiedEmail': profile.verifiedEmail})

    return redirect_to(request, '/auth/login/', permanent=False)

def help(request, helpMessageId = ''):
    if(helpMessageId in HELP_MESSAGES):
        return HttpResponse(createXmlSuccessResponse(HELP_MESSAGES[helpMessageId]), content_type='application/xml')

    return HttpResponse(createXmlErrorResponse('Help topic not found'), content_type='application/xml')