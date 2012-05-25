from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives, BadHeaderError

def sendMail(subject, toMail, fromEmail, htmlContentTemplate, 
             linkInitialPart, code, user, textContent):
    htmlContent = get_template(htmlContentTemplate)
    verifyEmailCode = code + '/'
    link = linkInitialPart + verifyEmailCode
    context = Context({'link': link, 'user': user})
    email = EmailMultiAlternatives(subject, textContent, fromEmail, [toMail])
    email.attach_alternative(htmlContent.render(context), 'text/html')
    try:
        email.send()
        return True
    except BadHeaderError:
        print 'bad header error'
    except:
        print 'another problem'
    return False