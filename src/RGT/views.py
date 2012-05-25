from django.shortcuts import render
from django.views.generic.simple import redirect_to
#import logging

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
