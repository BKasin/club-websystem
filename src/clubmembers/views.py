from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .models import Member, Membership, PendingEmailChange
from .forms import MemberForm

# Create your views here.
@transaction.atomic   # A database transaction is used for this entire function
@login_required
def userprofile(request):
  member = request.user
  if not request.method == 'POST':
    # Initial load of the form; populate from the existing Member instance
    form = MemberForm(instance=member)

  else:
    # User posted changes; populate the form from those changes instead,
    #   but still bind to the member instance
    form = MemberForm(request.POST, request.FILES, instance=member)

    if form.is_valid():
      if 'email' in form.changed_data:
        oldemail = form.initial['email']
        newemail = form.cleaned_data['email']

        # Don't let the user change the email yet. The new one must be confirmed.
        changerequest = PendingEmailChange.objects.create_pendingemail(member)
        confirmation_key = changerequest.confirmation_key
        form.instance.email = oldemail
        form.instance.email_pending = newemail

        # Save the Member instance
        form.instance.save()

        # Notify the old email address of the change
        context = Context({
          'user': member,
        })
        template_txt = get_template('changeofemail_old_email.txt')
        template_html = get_template('changeofemail_old_email.html')
        msg = EmailMultiAlternatives(
          subject='Your email has been changed',
          body=template_txt.render(context),
          from_email=settings.DEFAULT_FROM_EMAIL,
          to=[oldemail]
        )
        msg.attach_alternative(template_html.render(context), 'text/html')
        msg.send()

        # Send activation link to new email address
        context = Context({
          'user': member,
          'expiration_days': settings.PENDINGEMAIL_CONFIRMATION_DAYS,
          'confirmation_key': confirmation_key
        })
        template_txt = get_template('changeofemail_new_email.txt')
        template_html = get_template('changeofemail_new_email.html')
        msg = EmailMultiAlternatives(
          subject='Activate your new email',
          body=template_txt.render(context),
          from_email=settings.DEFAULT_FROM_EMAIL,
          to=[newemail]
        )
        msg.attach_alternative(template_html.render(context), 'text/html')
        msg.send()

        # Add a message to the user
        messages.success(request, "Changes made successfully.")
        messages.warning(request, "Email change is pending activation (see below).")

      else:
        # Save the Member instance
        form.instance.save()

        # Add a message to the user
        messages.success(request, "Changes made successfully.")

      # Everything looks good, so redirect the user to their updated profile page
      return redirect(userprofile)

    else:
      # Validation errors on the form, so show the errors instead of redirecting
      messages.error(request, "Changes not applied. Please correct the errors hilighted below.")

  # Lookup all memberships, except if they expired more than 180 days ago
  context = {
    'form': form,
    'membershiplist': Membership.objects.filter(member = member.id,
                        paid_until_date__gte = (datetime.today() - timedelta(days=180)))
  }
  return render(request, "userprofile.html", context)

@transaction.atomic   # A database transaction is used for this entire function
@login_required
def confirmemail(request, confirmation_key):
  profile = PendingEmailChange.objects.confirm_pendingemail(confirmation_key)
  if profile:
    messages.success(request, "Your new email has been confirmed and is now the active email for your account.")
  else:
    messages.error(request, "Your new email could not be activated.")
  return redirect(userprofile)
