from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from transactionalemail import mailer

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
        mailer.send_template_email(request,
          template_prefix='changeofemail_old_email',
          to=[oldemail],
          extra_context={'user': member}
        )

        # Send activation link to new email address
        mailer.send_template_email(request,
          template_prefix='changeofemail_new_email',
          to=[newemail],
          extra_context={
            'user': member,
            'expiration_days': settings.PENDINGEMAIL_CONFIRMATION_DAYS,
            'confirmation_key': confirmation_key,
          }
        )

        # Add a message to the user
        messages.success(request, "Changes made successfully.")
        messages.warning(request, "Email change is pending activation (see below).")

      else:  # NOT if 'email' in form.changed_data
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
