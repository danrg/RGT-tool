class CaptchaSecuredFormViewMixin(object):
    def get_form(self, form_class):
        if self.request.method in ('POST', 'PUT'):
            return form_class(self.request.POST, request = self.request)

        return form_class()