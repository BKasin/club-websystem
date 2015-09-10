from django.shortcuts import render
from django.db import models
from CommonMark.CommonMark import DocParser, HTMLRenderer

# Create your views here.
from .models import Content

# Create your views here.
def pagemd(request, page):
  #try:
  contentblock = Content.objects.get(uniquetitle=page)
  #except models.DoesNotExist:
  #  context = {
  #    "renderedmd": "Page could not be found"
  #  }
  #  return render(request, "infosec/pagemd.html", context)

  parser = DocParser()
  ast = parser.parse(contentblock.blob)
  renderer = HTMLRenderer()
  context = {
    "renderedmd": renderer.render(ast)
  }
  return render(request, "infosec/pagemd.html", context)
