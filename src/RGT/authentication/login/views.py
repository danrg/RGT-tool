from django.shortcuts import render_to_response
from django.template import RequestContext
from loginForm import LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout as djangoLogout
from django.contrib.auth import login as djangoLogin
from django.views.generic.simple import redirect_to

def login(request):

    if request.user.is_authenticated():
        return redirect_to(request, '/home/') # User is already logged in, redirect to home.
    
    if request.method == 'POST':
        form= LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(email= form.cleaned_data['email'], password= form.cleaned_data['password'])

            if user is not None:
                # Authentication success
                djangoLogin(request, user);
                return redirect_to(request, '/home/') # User successfully authenticated, redirect to home.'
    else:
        form= LoginForm() # GET Request, prepare an empty form.
        
    return render_to_response('authentication/login.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def logout(request):
    # Django logout
    djangoLogout(request)

    #Redirect to login screen
    return redirect_to(request, '/auth/login/')