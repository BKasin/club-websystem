from django.shortcuts import render, redirect
from django.db import models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import Http404
from django.utils.html import format_html
from django.core.urlresolvers import reverse

from CommonMark.CommonMark import DocParser, HTMLRenderer

from .models import Block
from .forms import BlockForm

NAVBAR_BLOCK_ID = 'navbar'



def wrap_blob_with_editablediv(blob, uniquetitle):
  return ("<div class='editableblock'><a class='editblockbutton' href='{}'>edit the '{}' block</a>".format(reverse('contentblock_edit', args=(uniquetitle,)), uniquetitle) + blob + "</div>")

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
  user_auth = user.is_authenticated()
  may_edit = user_auth and user.may_edit_blocks

  try:
    # Because Block has a custom manager, the results are filtered already even before adding this filter
    contentblock = Block.objects.get(uniquetitle=page)
  except Block.DoesNotExist:
    if may_edit:
      # Only users who may edit blocks may create a new one
      return redirect(contentblock_edit, page)
    else:
      raise Http404()

  # If a block is not yet published, the user should not even know it exists
  if not contentblock.published:
    if may_edit:
      messages.warning(request, "This block has not yet been published.")
    else:
      raise Http404()

  # Certain blocks may be marked as auth_required
  if contentblock.auth_required and not user_auth:
    messages.warning(request, "You must be logged in to view that page.")
    return redirect_to_login(request.path)

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
  user = request.user
  if not user.may_edit_blocks:  # No need to check is_authenticated here, since @login_required is already specified above
    raise Http404("You do not have privileges to edit content blocks.")

  if request.method == 'POST':
    # User posted changes
    try:
      contentblock = Block.objects.get(uniquetitle=page)
    except Block.DoesNotExist:
      # Block doesn't exist, so we'll create a new one
      contentblock = Block(uniquetitle=page, site=Site.objects.get_current())
    form = BlockForm(request.POST, instance=contentblock)

    if form.is_valid():
      # messages.success(request, str(form.instance.available_to_groups) + " <-> " + str(form.cleaned_data['available_to_groups']))
      # form.instance.available_to_groups = form.cleaned_data['available_to_groups']
      form.instance.save()

      messages.success(request, "Changes made successfully.")
      return redirect(contentblock_view, page)
    else:  # form.is_valid() failed
      messages.error(request, "Form data is not valid.")

  else:  # request.method is GET
    # Initial load of the form
    try:
      contentblock = Block.objects.get(uniquetitle=page)
    except Block.DoesNotExist:
      messages.warning(request, "This block does not yet exist, but you may create it below.")
      contentblock = Block(uniquetitle=page, site=Site.objects.get_current())
    form = BlockForm(instance=contentblock)

  context = {
    'form': form,
    'uniquetitle': page,
    'title': contentblock.description,
    'blob': contentblock.blob,
  }
  return render(request, "contentblock_edit.html", context)
