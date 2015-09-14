from django.shortcuts import render
from django.db import models
from django.http import HttpResponse, Http404
from CommonMark.CommonMark import DocParser, HTMLRenderer

# Create your views here.
from .models import Content

# Create your views here.
def pagemd(request, page):
  try:
    contentblock = Content.objects.get(uniquetitle=page)
  except Content.DoesNotExist:
    raise Http404("Content block named %s could not be found."%(page))

  parser = DocParser()
  ast = parser.parse(contentblock.blob)
  renderer = HTMLRenderer()
  context = {
    "renderedmd": renderer.render(ast)
  }
  return render(request, "infosec/pagemd.html", context)
