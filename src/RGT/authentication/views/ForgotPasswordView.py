from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from RGT.authentication.forms.ForgotPasswordForm import ForgotPasswordForm
from RGT import settings
from RGT.authentication.models import PassRecoverCode
from RGT.gridMng import utility
from RGT.utils import sendMail

class ForgotPasswordView(FormView):
    template_name = 'authentication/forgotPass.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')

        return super(ForgotPasswordView, self).get(self, request, *args, **kwargs);

    def get_form(self, form_class):
        if self.request.method in ('POST', 'PUT'):
            return ForgotPasswordForm(self.request.POST, request = self.request)

        return ForgotPasswordForm()

    def form_invalid(self, form):
        return super(ForgotPasswordView, self).form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        # send the email for the new password request
        subject = 'New password request for RGT!'
        toMail = form.cleaned_data['email']
        htmlContentTemplate = 'authentication/forgotPassEmail.html'
        linkInitialPart = settings.HOST_NAME+'/accounts/recover/'
        generatedCode = utility.randomStringGenerator(14)
        textContent = 'Click this link to change your password.'
        fromMail = settings.EMAIL_HOST_USER
        if sendMail(subject, toMail, fromMail, htmlContentTemplate, linkInitialPart,
            generatedCode, user, textContent):
            code = PassRecoverCode()
            code.email = toMail
            code.linkCode = generatedCode
            code.save()
            return self.render_to_response(self.get_context_data(form=form, checkEmail = True))
        else:
            # error in sending mail
            pass

        return super(ForgotPasswordView, self).form_valid(form)