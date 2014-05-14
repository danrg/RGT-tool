from django.contrib.auth.models import User
from RGT.authentication.forms.ForgotPasswordForm import ForgotPasswordForm
from RGT.authentication.models import PassRecoverCode
from RGT.authentication.EmailService import EmailService
from RGT.gridMng.utility import generateRandomString
from RGT.authentication.views.CaptchaSecuredFormView import CaptchaSecuredFormView


class ForgotPasswordView(CaptchaSecuredFormView):
    template_name = 'authentication/forgotPass.html'
    form_class = ForgotPasswordForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)

        code = PassRecoverCode()
        code.email = email
        code.linkCode = generateRandomString(14)

        emailService = EmailService()

        if emailService.sendForgotPasswordEmail(user, code):
            code.save()
            return self.render_to_response(self.get_context_data(form=form, checkEmail=True))
        else:
            # error in sending mail
            pass

        return super(ForgotPasswordView, self).form_valid(form)