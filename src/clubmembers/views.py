from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Member
from .forms import MemberForm

# Create your views here.
@login_required
def userprofile(request):
  user = request.user
  member = user.member
  context = {}
  initialdata = {'username': user.username, 'password': user.password}
  if request.method == 'POST':
    form = MemberForm(request.POST, request.FILES, instance=member, initial=initialdata)
    context['form'] = form
    if form.is_valid():
      newusername = form.cleaned_data['username']
      user = form.instance.user
      if (user.username != newusername):
        user.username = newusername
        user.save()
      form.instance.save()
      context['success'] = True
    else:
      context['fail'] = True

  else:
    form = MemberForm(instance=member, initial=initialdata)
    context['form'] = form

  return render(request, "infosec/userprofile.html", context)
