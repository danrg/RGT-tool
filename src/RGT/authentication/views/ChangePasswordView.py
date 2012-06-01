from django.views.generic.edit import FormView
from RGT.authentication.forms import ChangePasswordForm
from RGT import AuthorizedView
from RGT.authentication.views.CaptchaSecuredFormViewMixin import CaptchaSecuredFormViewMixin

class ChangePasswordView(FormView, AuthorizedView, CaptchaSecuredFormViewMixin):
    template_name = 'authentication/changePass.html'
    form_class = ChangePasswordForm

    def form_valid(self, form):
        user = self.request.user

        user.set_password(form.cleaned_data['newPassword'])
        user.save()

        return self.render_to_response(self.get_context_data(form=form, passUpdated = True))