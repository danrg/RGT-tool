from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from RGT import settings


class EmailService(object):
    def sendForgotPasswordEmail(self, user, passRecoverCode):
        # send the email for the new password request
        subject = 'New password request for RGT!'
        htmlContentTemplate = 'authentication/forgotPassEmail.html'
        linkInitialPart = settings.HOST_NAME + '/accounts/recover/'

        verifyEmailCode = passRecoverCode.linkCode + '/'
        link = linkInitialPart + verifyEmailCode

        htmlContent = get_template(htmlContentTemplate)
        context = Context({'link': link, 'user': user})

        return self.prepareAndSendEmail(subject, passRecoverCode.email, htmlContent.render(context))

    def sendRegistrationEmail(self, user, verificationCode):
        subject = 'Email verification for RGT!'
        htmlContentTemplate = 'authentication/verifyEmail.html'

        linkInitialPart = settings.HOST_NAME + '/auth/verify/'
        link = linkInitialPart + verificationCode + '/'

        htmlContent = get_template(htmlContentTemplate)
        context = Context({'link': link, 'user': user})

        return self.prepareAndSendEmail(subject, user.email, htmlContent.render(context))

    def prepareAndSendEmail(self, subject, toMail, htmlContent):
        fromMail = settings.EMAIL_HOST_USER
        email = EmailMultiAlternatives(subject, None, fromMail, [toMail])
        email.attach_alternative(htmlContent, 'text/html')

        return self.sendEmail(email)

    def sendEmail(self, email):
        try:
            email.send()
            return True

        except BadHeaderError:
            print 'bad header error'
        except Exception:
            print 'another problem'

        return False


