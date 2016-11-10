from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.query import Prefetch
from django.contrib.sites.models import Site

from clubmembers.models import Member, Membership

@login_required
def membershipmanager(request):
  # Get current club
  current_site = Site.objects.get_current()
  if not current_site.has_club: raise Exception('Current site has no club')
  current_club_id = current_site.club.id

  # Get list of all Members
  members = Member.objects.order_by('name_first') \
    .prefetch_related(Prefetch(   # While we're at it, prefetch the entire list of Memberships for the current club too, sorted in reverse by their expiration dates
      'membership_set',
      queryset=Membership.objects.filter(club=current_club_id).order_by('-paid_until_date')
    )) \
    .prefetch_related(            # While we're at it, also prefetch the club list, so doesn't happen over and over as each Membership object is processed
      'membership_set__club'
    )

  for member in members:
    m = member.membership_set.all()
    if m.count()==0:
      member.most_recent_membership = None
      member.list = 2
    else:
      member.most_recent_membership = m[0]
      member.list = 0 if member.most_recent_membership.is_active else 1

  # paidmembers = Member.objects.get()
  # paidmembers = []
  # for member in members:
  # paidmembers.append(member)

  context = {
    'members': members,
    # 'paidmembers': paidmembers,
  }
  return render(request, "membership_manage.html", context)


  # @property
  # def most_recent_membership(self):
  #   # return self.membership_set.latest('paid_until_date')
  #   return self.membership_set.all()
