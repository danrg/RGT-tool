from django.shortcuts import redirect
from ...userProfile.models import UserProfile
from django.contrib.auth.models import User


def verify(request, verifyEmailCode=''):
    if request.method == 'GET':
        code = verifyEmailCode
        profile = UserProfile.objects.get(verifyEmailCode=code)
        user_email = profile.user
        if not profile.verifiedEmail:
            profile.verifiedEmail = True
            profile.save()
            user = User.objects.get(email=user_email)
            user.is_active = True
            user.save()
        else:
        # profile already verified
            pass

    return redirect('/auth/login/')
