from django.conf import settings
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import get_template

from .contactForm import ContactForm


def contact(request):
    if not request.user.is_authenticated():
        return redirect('/auth/login/')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            toMail = [settings.EMAIL_HOST_USER]
            sender = form.cleaned_data['email']
            content = form.cleaned_data['content']
            html_content = get_template('contact/contactEmail.html')
            context = {'email': sender, 'content': content}
            rendered_html = html_content.render(context)

            email = EmailMultiAlternatives(subject, rendered_html, sender, toMail)
            email.attach_alternative(rendered_html, 'text/html')
            try:
                email.send()
                request.session['didContact'] = True
                return HttpResponseRedirect('/contact/')
            except BadHeaderError:
                print 'bad header error'
            except:
                print 'another problem'
        else:
            return render(request,
                          'contact/contact.html',
                          {'form': form})
    else:
        form = ContactForm()
        did_contact = request.session.get('didContact')
        if did_contact is not None:
            del request.session['didContact']

        return render(request,
                      'contact/contact.html',
                      {'form': form, 'didContact': did_contact})
