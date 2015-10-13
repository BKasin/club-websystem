from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from transactionalemail import mailer

from .forms import ContactForm

from clubmembers.models import Member

# Create your views here.
def home(request):
  return render(request, "home.html")

def about(request):
  form = ContactForm(request.POST or None)

  if form.is_valid():
    senderemail = form.cleaned_data['email']
    mailer.send_template_email(request,
      template_prefix='contact_email',
      to=settings.GENERIC_CONTACT_EMAIL,
      reply_to=[senderemail],
      extra_context={
        'sendername': form.cleaned_data['full_name'],
        'senderemail': senderemail,
        'message': form.cleaned_data['message'],
      }
    )

    messages.success(request, "Your email has been sent successfully.")
    return redirect(about)

  context = {
    "form": form,
  }
  return render(request, "about.html", context)
