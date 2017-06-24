from django.views.generic.edit import FormView


class CaptchaSecuredFormView(FormView):
    def get_form(self):
        if self.request.method in ('POST', 'PUT'):
            return self.form_class(self.request.POST, request=self.request)

        return self.form_class()
