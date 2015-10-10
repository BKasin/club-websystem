from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from CommonMark.CommonMark import DocParser, HTMLRenderer

# Create your views here.
from .models import Block
from .forms import BlockForm

# Create your views here.
def pagemd(request, page):
  contentblock = get_object_or_404(Block, uniquetitle=page)

  editable = request.user.has_perm('contentblocks.change_block')
  blob = contentblock.blob

  parser = DocParser()
  ast = parser.parse(blob)
  renderer = HTMLRenderer()

  context = {
    'editable': editable,
    'uniquetitle': page,
    'renderedmd': renderer.render(ast),
  }
  return render(request, "pagemd.html", context)

@login_required
def pagemdedit(request, page):
  contentblock = get_object_or_404(Block, uniquetitle=page)
  editable = request.user.has_perm('contentblocks.in_page_editor')
  if not editable:
    raise Http404("You do not have privileges to edit content block %s."%(page))

  if not request.method == 'POST':
    # Initial load of the form
    form = BlockForm(instance=contentblock)

  else:
    # User posted changes
    form = BlockForm(request.POST, instance=contentblock)

    if form.is_valid():
      form.instance.save()
      messages.success(request, "Changes made successfully.")
      return redirect(pagemd, page)
    else:
      messages.error(request, "Form data is not valid.")

  context = {
    'form': form,
    'uniquetitle': page,
    'blob': contentblock.blob,
  }
  return render(request, "pagemdedit.html", context)
