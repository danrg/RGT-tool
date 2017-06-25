import datetime

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.timezone import utc

from .recoverPassForm import RecoverPassForm


def recoverPass(request, passRecoverCode=''):
    from ..models import PassRecoverCode
    from django.contrib.auth.models import User

    if request.user.is_authenticated():
        return redirect('/home/')

    if request.method == 'POST':
        # POSTed the new password
        post_link_code = request.POST['linkCode']
        form = RecoverPassForm(request.POST)
        form.full_clean()
        try:
            code = PassRecoverCode.objects.get(linkCode=post_link_code)
            if code.linkUsed is False and code.linkExpired is False:
                invalid_link = False
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
                    return render(request,
                                  'authentication/recoverPassword.html',
                                  {'form': form, 'invalidLink': invalid_link, 'linkCode': code.linkCode})
            else:
                # code has been used
                invalid_link = True
        except PassRecoverCode.DoesNotExist:
            # code does not exist
            invalid_link = True

        return render(request,
                      'authentication/recoverPassword.html',
                      {'invalidLink': invalid_link})
    else:
        # GET request
        # check if the link is still active
        try:
            code = PassRecoverCode.objects.get(linkCode=passRecoverCode)
            if code.linkUsed is False:
                # check date time of the code if it has expired
                code_date = code.dateTime
                now = datetime.datetime.utcnow().replace(tzinfo=utc)
                elapsed_code_date = now - code_date

                # link is valid for 4 hours
                if elapsed_code_date.seconds / 60 < 240:
                    form = RecoverPassForm()
                    invalid_link = False

                    context = {'form': form,
                               'invalidLink': invalid_link,
                               'linkCode': code.linkCode}
                    return render(request,
                                  'authentication/recoverPassword.html',
                                  context)
                else:
                    # probably this should not happen here, we should check the time
                    # somehow different. maybe with a script in the database
                    # code has expired
                    invalid_link = True
                    code.linkExpired = True
                    code.save()
            else:
                # code has been already used
                invalid_link = True
        except PassRecoverCode.DoesNotExist:
            # code does not exist
            invalid_link = True

        return render(request,
                      'authentication/recoverPassword.html',
                      {'invalidLink': invalid_link})
