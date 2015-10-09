from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta

from .models import Member, Membership
from .forms import MemberForm

# Create your views here.
@login_required
def userprofile(request):
  member = request.user
  if not request.method == 'POST':
    # Initial load of the form; populate from the existing Member instance
    form = MemberForm(instance=member)

  else:
    # User posted changes; populate the form from those changes instead, but still bind to the member instance
    form = MemberForm(request.POST, request.FILES, instance=member)

    if form.is_valid():
      if 'email' in form.changed_data:
        # Don't let the user change the email yet. The new one must be confirmed.
        form.instance.email = form.initial['email']
        form.instance.email_pending = form.cleaned_data['email']
        addpendingemailwarning = True
      else:
        addpendingemailwarning = False

      # Save the Member instance
      form.instance.save()

      # Everything looks good, so redirect the user to their updated profile page
      messages.success(request, "Changes made successfully.")
      if addpendingemailwarning: messages.warning(request, "Email change is pending activation (see below).")
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
