from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import Http404
from django.utils.html import format_html
from django.core.urlresolvers import reverse

from CommonMark.CommonMark import DocParser, HTMLRenderer

from .models import Block
from .forms import BlockForm

NAVBAR_BLOCK_ID = 'navbar'
navdata = None

def get_navdata():
  return navdata

def set_navdata(nd):
  global navdata
  navdata = nd



def wrap_blob_with_editablediv(blob, uniquetitle):
  return ("<div class='editableblock'><a class='editblockbutton' href='" +
          reverse('contentblock_edit', args=(uniquetitle,)) +
          "'>edit this block</a>" +
          blob + "</div>")

def render_blob(blob, datatype):
  # This must return a string that is ready to insert directly into the page, without any further escaping
  try:
    if datatype == Block.MARKDOWN:
      parser = DocParser()
      ast = parser.parse(blob)
      renderer = HTMLRenderer()
      # No escaping, since markdown has already parsed everything
      return '<div class="markdown-body">%s</div>' % renderer.render(ast)
    elif datatype == Block.HTML:
      # No escaping; we want the original
      return blob
    elif datatype == Block.TEXT:
      # Escape the blob, so all characters will be preserved
      return format_html('<div style="white-space:pre-wrap">{}</div>', blob)
    elif datatype == Block.JSON:
      return '{No rendering for JSON blobs}'
    else:
      return '{Unable to render block}'
  except:
    return '{Error rendering block}'

def contentblock_view(request, page):
  user = request.user
  may_edit = request.user.is_authenticated() and request.user.may_edit_blocks

  try:
    # Because Block has a custom manager, the results are filtered already even before adding this filter
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

  blob = render_blob(contentblock.blob, contentblock.datatype)
  if may_edit: blob = wrap_blob_with_editablediv(blob, page)

  context = {
    'uniquetitle': page,
    'title': contentblock.description,
    'renderedblob': blob,
  }
  return render(request, "contentblock_view.html", context)

@login_required
def contentblock_edit(request, page):
  if not request.user.may_edit_blocks:  # No need to check is_authenticated, since login is already required
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
      # TODO: we need a more club-neutral way of doing this
      if page == NAVBAR_BLOCK_ID:
        global navdata
        navdata = None

      messages.success(request, "Changes made successfully.")
      return redirect(contentblock_view, page)
    else:
      messages.error(request, "Form data is not valid.")

  context = {
    'form': form,
    'uniquetitle': page,
    'title': contentblock.description,
    'blob': contentblock.blob,
  }
  return render(request, "contentblock_edit.html", context)
