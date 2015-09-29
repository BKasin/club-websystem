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
    context = Context({
      'sendername': form.cleaned_data.get("full_name"),
      'senderemail': form.cleaned_data.get("email"),
      'message': form.cleaned_data.get("message"),
    })
    template_txt = get_template('contact_email.txt')
    template_html = get_template('contact_email.html')

    msg = EmailMultiAlternatives(
      subject='Email from website contact form',
      body=template_txt.render(context),
      from_email='csusb.infosec.club@gmail.com',
      to=['testing2@infosec-csusb.org']
    )
    msg.attach_alternative(template_html.render(context), 'text/html')
    msg.send()

    return redirect('about')

  context = {
    "form": form,
  }
  return render(request, "about.html", context)
