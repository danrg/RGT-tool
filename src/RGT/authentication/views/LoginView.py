from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth import login as django_login
from ..forms import LoginForm


class LoginView(FormView):
    template_name = 'authentication/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')

        return super(LoginView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])

        if user is not None:
            # Authentication success
            django_login(self.request, user)
            return HttpResponseRedirect('/home/')
        else:
            form._errors['__all__'] = "Invalid username or password"
            return self.form_invalid(form)
