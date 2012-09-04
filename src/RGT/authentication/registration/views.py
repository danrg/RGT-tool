from django.views.generic.simple import redirect_to
from RGT.userProfile.models import UserProfile
from django.contrib.auth.models import User
from django.utils.functional import SimpleLazyObject

def verify(request, verifyEmailCode=''):
    if not request.user.is_authenticated():
        return redirect_to(request, '/auth/login/')
        
    if request.method == 'GET':
        if not request.user.is_superuser:
            try:
                profile = UserProfile.objects.get(user=request.user)
                if profile.verifyEmailCode == verifyEmailCode:
                    if not profile.verifiedEmail:
                        profile.verifiedEmail = True
                        profile.save()
                        user = User.objects.get(id=request.user.id)
                        user.is_active = True
                        user.save()
                else:
                    # it is not the same user as the one logged in
                    pass
            except UserProfile.DoesNotExist:
                # a profile with this user does not exist
                pass
        
        return redirect_to(request, '/home/')
