from django.views.generic.edit import FormView


class CaptchaSecuredFormView(FormView):
    def get_form(self, form_class):
        if self.request.method in ('POST', 'PUT'):
            return form_class(self.request.POST, request=self.request)

        return form_class()