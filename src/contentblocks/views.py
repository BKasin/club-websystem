from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import Http404

from CommonMark.CommonMark import DocParser, HTMLRenderer

from mainsite.templatetags import infosec

from .models import Block
from .forms import BlockForm

# Create your views here.
def contentblock_view(request, page):
  may_edit = request.user.may_edit_blocks

  try:
    # Because Block has a custom manager, the results will already be filtered to the current site
    #   plus global items (not linked to any site)
    contentblock = Block.objects.get(uniquetitle=page)
  except Block.DoesNotExist:
    if may_edit:
      return redirect(contentblock_edit, page)
    else:
      raise Http404()

  if not contentblock.published:
    if may_edit:
      messages.warning(request, "This block has not yet been published.")
    else:
      raise Http404()

  parser = DocParser()
  ast = parser.parse(contentblock.blob)
  renderer = HTMLRenderer()

  context = {
    'uniquetitle': page,
    'renderedmd': renderer.render(ast),
  }
  return render(request, "contentblock_view.html", context)

@login_required
def contentblock_edit(request, page):
  if not request.user.may_edit_blocks:
    raise Http404("You do not have privileges to edit content blocks.")

  if not request.method == 'POST':
    # Initial load of the form
    try:
      contentblock = Block.objects.get(uniquetitle=page)
    except Block.DoesNotExist:
      messages.warning(request, "This block does not yet exist, but you may create it below.")
      contentblock = Block(uniquetitle=page, site=Site.objects.get_current())

    form = BlockForm(instance=contentblock)

  else:
    # User posted changes
    try:
      contentblock = Block.objects.get(uniquetitle=page)
    except Block.DoesNotExist:
      contentblock = Block(uniquetitle=page, site=Site.objects.get_current())
    form = BlockForm(request.POST, instance=contentblock)

    if form.is_valid():
      form.instance.save()

      # If we just changed the navbar, trigger a refresh of it
      if contentblock.uniquetitle == infosec.NAVBAR_BLOCK_ID:
        infosec.navdata = None

      messages.success(request, "Changes made successfully.")
      return redirect(contentblock_view, page)
    else:
      messages.error(request, "Form data is not valid.")

  context = {
    'form': form,
    'uniquetitle': page,
    'blob': contentblock.blob,
  }
  return render(request, "contentblock_edit.html", context)
