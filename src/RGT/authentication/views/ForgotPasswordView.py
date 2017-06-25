from django.contrib.auth.models import User
from ..forms.ForgotPasswordForm import ForgotPasswordForm
from ..models import PassRecoverCode
from ..EmailService import EmailService
from ...gridMng.utility import generateRandomString
from ..views.CaptchaSecuredFormView import CaptchaSecuredFormView


class ForgotPasswordView(CaptchaSecuredFormView):
    template_name = 'authentication/forgotPass.html'
    form_class = ForgotPasswordForm
    success_url = '/home'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)

        code = PassRecoverCode()
        code.email = email
        code.linkCode = generateRandomString(14)

        email_service = EmailService()

        if email_service.sendForgotPasswordEmail(user, code):
            code.save()
            return self.render_to_response(self.get_context_data(form=form, checkEmail=True))
        else:
            # error in sending mail
            pass

        return super(ForgotPasswordView, self).form_valid(form)
