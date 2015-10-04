from django.shortcuts import render
from django.db import models
from django.http import HttpResponse, Http404
from CommonMark.CommonMark import DocParser, HTMLRenderer

# Create your views here.
from .models import Block

# Create your views here.
def pagemd(request, page, editmode=False):
  try:
    contentblock = Block.objects.get(uniquetitle=page)
  except Block.DoesNotExist:
    raise Http404("Content block named %s could not be found."%(page))

  blob = contentblock.blob

  editable = request.user.has_perm('contentblocks.in_page_editor')

  if editmode:
    context = {
      'editmode': editmode,
      'uniquetitle': page,
      'origmd': blob,
    }
    return render(request, "pagemdedit.html", context)

  else:
    parser = DocParser()
    ast = parser.parse(blob)
    renderer = HTMLRenderer()
    context = {
      'editmode': editmode,
      'editable': editable,
      'uniquetitle': page,
      'origmd': blob,
      'renderedmd': renderer.render(ast),
    }
    return render(request, "pagemd.html", context)
