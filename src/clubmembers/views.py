from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Member
from .forms import MemberForm

# Create your views here.
def userprofile(request):
  m = Member.objects.get(pk=1)
  if request.method == 'POST':
    form = MemberForm(request.POST, instance=m)
    if form.is_valid():
      print("Saving...")
      form.instance.save()
      return HttpResponseRedirect('/userprofile/')
  else:
    form = MemberForm(instance=m)

  context = {
    'form': form
  }
  return render(request, "infosec/userprofile.html", context)
