from django.shortcuts import redirect


def verify(request, verifyEmailCode=''):
    if request.method == 'GET':
        code = verifyEmailCode

        from django.contrib.auth.models import User
        from ...userProfile.models import UserProfile
        profile = UserProfile.objects.get(verifyEmailCode=code)
        user_email = profile.user

        if not profile.verifiedEmail:
            profile.verifiedEmail = True
            profile.save()
            user = User.objects.get(email=user_email)
            user.is_active = True
            user.save()

    return redirect('/auth/login/')
