from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Member
from .forms import MemberForm

# Create your views here.
@login_required
def userprofile(request):
  member = request.user
  if not request.method == 'POST':
    # Initial load of the form; populate from the existing Member instance
    form = MemberForm(instance=member)
    context = {
      'form': form,
    }
  else:
    # User posted changes; populate the form from those changes instead, but still bind to the member instance
    form = MemberForm(request.POST, request.FILES, instance=member)
    if form.is_valid():
      # Save the Member instance
      form.instance.save()

      # Everything looks good, so redirect the user to their updated profile page
      #return redirect('userprofile')
      return render(request, "userprofile_changed.html") #Temporary, until we use message properly

    else:
      # Validation errors on the form, so show the errors instead of redirecting
      context = {
        'form': form,
        'fail': True,
      }

  return render(request, "userprofile.html", context)
