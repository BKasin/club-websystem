from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Member
from .forms import MemberForm

# Create your views here.
@login_required
def userprofile(request):
  user = request.user
  member = user.member
  initialdata = {'username': user.username, 'password': user.password}
  if request.method == 'POST':
    form = MemberForm(request.POST, request.FILES, instance=member, initial=initialdata)
    if form.is_valid():
      newusername = form.cleaned_data['username']
      user = form.instance.user
      if (user.username != newusername):
        user.username = newusername
        user.save()
      form.instance.save()
      return redirect('userprofile')
    else:
      context = {
        'form': form,
        'fail': True,
      }
  else:
    form = MemberForm(instance=member, initial=initialdata)
    context = {
      'form': form,
    }

  return render(request, "userprofile.html", context)
