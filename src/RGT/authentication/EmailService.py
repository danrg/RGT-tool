from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from .. import settings


class EmailService(object):
    def send_forgot_password_email(self, user, pass_recover_code):
        # send the email for the new password request
        subject = 'New password request for RGT!'
        html_content_template = 'authentication/forgotPassEmail.html'
        link_initial_part = settings.HOST_NAME + '/accounts/recover/'

        verify_email_code = pass_recover_code.linkCode + '/'
        link = link_initial_part + verify_email_code

        html_content = get_template(html_content_template)
        context = {'link': link, 'user': user}

        html_render = html_content.render(context)
        return self.prepare_send_email(subject, pass_recover_code.email, html_render)

    def send_registration_email(self, user, verificationCode):
        subject = 'Email verification for RGT!'
        html_content_template = 'authentication/verifyEmail.html'

        link_initial_part = settings.HOST_NAME + '/auth/verify/'
        link = link_initial_part + verificationCode + '/'

        html_content = get_template(html_content_template)
        context = Context({'link': link, 'user': user})

        return self.prepare_send_email(subject, user.email, html_content.render(context))

    def prepare_send_email(self, subject, to_mail, html_content):
        from_mail = settings.EMAIL_HOST_USER
        email = EmailMultiAlternatives(subject, html_content, from_mail, [to_mail])
        email.attach_alternative(html_content, 'text/html')

        return self.sendEmail(email)

    def sendEmail(self, email):
        try:
            email.send()
            return True

        except BadHeaderError:
            print 'bad header error'
        except Exception as e:
            print 'another problem: ' + str(e.args[0]) + ' - ' + str(e.args[1])

        return False
