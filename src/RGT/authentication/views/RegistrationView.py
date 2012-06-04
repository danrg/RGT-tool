from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from RGT.authentication.EmailService import EmailService
from RGT.gridMng import utility
from RGT.authentication.forms import RegistrationForm
from RGT.authentication.views.CaptchaSecuredFormViewMixin import CaptchaSecuredFormViewMixin

class RegistrationView(FormView, CaptchaSecuredFormViewMixin):
    template_name = "authentication/register.html"
    success_url = "/home"
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')

        return super(RegistrationView, self).get(self, request, *args, **kwargs);

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        firstName = form.cleaned_data['firstName']
        lastName = form.cleaned_data['lastName']

        user = User.objects.create_user(email, email, password);
        user.first_name = firstName
        user.last_name = lastName
        user.is_active = False
        user.save();

        #login the user after creation
        user = authenticate(email= email, password= password)
        login(self.request, user);

        verificationCode = utility.randomStringGenerator(14)

        profile = user.get_profile()
        profile.verifyEmailCode = verificationCode

        emailService = EmailService()
        if emailService.sendRegistrationEmail(user, verificationCode):
            profile.save();
            return HttpResponseRedirect('/home/');
        else:
            # problem with email sending
            pass

        return super(RegistrationView, self).form_valid(form)


