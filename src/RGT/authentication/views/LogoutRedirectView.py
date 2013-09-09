from django.contrib.auth import logout
from django.views.generic.base import RedirectView


class LogoutRedirectView(RedirectView):
    permanent = False
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutRedirectView, self).get(request, *args, **kwargs)