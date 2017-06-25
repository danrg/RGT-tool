from ... import AuthorizedView
from ..forms import ChangePasswordForm
from ..views.CaptchaSecuredFormView import CaptchaSecuredFormView


class ChangePasswordView(AuthorizedView, CaptchaSecuredFormView):
    template_name = 'authentication/changePass.html'
    form_class = ChangePasswordForm

    def form_valid(self, form):
        user = self.request.user

        user.set_password(form.cleaned_data['newPassword'])
        user.save()

        return self.render_to_response(self.get_context_data(form=form, passUpdated=True))
