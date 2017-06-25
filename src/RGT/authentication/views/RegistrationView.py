from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from ..EmailService import EmailService
from ...gridMng import utility
from django.conf import settings
from ..forms import RegistrationForm
from .CaptchaSecuredFormView import CaptchaSecuredFormView


class RegistrationView(CaptchaSecuredFormView):
    template_name = "authentication/register.html"
    success_url = "/home"
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')

        captcha_view = super(RegistrationView, self)
        return captcha_view.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['firstName']
        last_name = form.cleaned_data['lastName']

        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        if settings.EMAIL_VERIFICATION:
            user.is_active = False
        user.save()

        # login the user after creation
        user = authenticate(email=email, password=password)
        login(self.request, user)

        verification_code = utility.generateRandomString(14)
        user.profile.verifyEmailCode = verification_code

        email_service = EmailService()
        if email_service.sendRegistrationEmail(user, verification_code):
            user.profile.save()
            return HttpResponseRedirect('/home/')

        return super(RegistrationView, self).form_valid(form)
