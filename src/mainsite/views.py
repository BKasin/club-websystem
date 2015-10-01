from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .forms import ContactForm

from clubmembers.models import Member

# Create your views here.
def home(request):
  return render(request, "home.html")

def about(request):
  form = ContactForm(request.POST or None)

  if form.is_valid():
    sendername = form.cleaned_data.get("full_name")
    senderemail = form.cleaned_data.get("email")
    context = Context({
      'sendername': sendername,
      'senderemail': senderemail,
      'message': form.cleaned_data.get("message"),
    })
    template_txt = get_template('contact_email.txt')
    template_html = get_template('contact_email.html')

    msg = EmailMultiAlternatives(
      subject='%s has sent a message through the website contact form' % sendername,
      body=template_txt.render(context),
      reply_to=[senderemail],
      from_email=settings.DEFAULT_FROM_EMAIL,
      to=['csusb.infosec.club@gmail.com']
    )
    msg.attach_alternative(template_html.render(context), 'text/html')
    msg.send()

    #return redirect('about')
    return render(request, "about_emailsent.html") #Temporary, until we use message properly

  context = {
    "form": form,
  }
  return render(request, "about.html", context)
