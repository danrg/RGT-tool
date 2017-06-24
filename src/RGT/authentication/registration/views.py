from django.shortcuts import redirect
from ...userProfile.models import UserProfile
from django.contrib.auth.models import User


def verify(request, verifyEmailCode=''):
    if request.method == 'GET':
        Code = verifyEmailCode
        profile = UserProfile.objects.get(verifyEmailCode=Code)
        useremail = profile.user
        if not profile.verifiedEmail:
            profile.verifiedEmail = True
            profile.save()
            user = User.objects.get(email=useremail)
            user.is_active = True
            user.save()
        else:
        # profile already verified
            pass

    return redirect('/auth/login/')
