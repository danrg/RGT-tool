from django.views.generic.edit import FormView
from RGT.authentication.forms import ChangePasswordForm

class ChangePasswordView(FormView):
    template_name = 'authentication/changePass.html'

    def form_valid(self, form):
        user = self.request.user

        user.set_password(form.cleaned_data['newPassword'])
        user.save()

        return self.render_to_response(self.get_context_data(form=form, passUpdated = True))

    def get_form(self, form_class):
        if self.request.method in ('POST', 'PUT'):
            return ChangePasswordForm(self.request.POST, request = self.request)

        return ChangePasswordForm()