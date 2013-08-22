from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context
from django.template.loader import get_template
#from django.views.generic.simple import redirect_to
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from RGT.contact.contactForm import ContactForm

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
            htmlContent = get_template('contact/contactEmail.html')
            context = Context({'email': sender, 'content': content})
            email = EmailMultiAlternatives(subject, '', sender, toMail)
            email.attach_alternative(htmlContent.render(context), 'text/html')
            try:
                email.send()
                request.session['didContact'] = True
                return HttpResponseRedirect('/contact/')
            except BadHeaderError:
                print 'bad header error'
            except:
                print 'another problem'
        else:
            return render_to_response('contact/contact.html',
                               {'form':form},
                               context_instance=RequestContext(request))
    else:
        form = ContactForm()
        didContact = request.session.get('didContact')
        if didContact != None:
            del request.session['didContact']
        
    return render_to_response('contact/contact.html',
                              {'form':form, 'didContact':didContact},
                              context_instance=RequestContext(request))
    
    
    