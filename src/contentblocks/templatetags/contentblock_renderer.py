import json
import fnmatch

from contentblocks.models import Block

from ..views import wrap_blob_with_editablediv, render_blob

from django import template
register = template.Library()

NAVBAR_BLOCK_ID = 'navbar'
navdata = None

def _generate_navbar(nd, curpage):
  output = ""
  for pgref in nd:
    pagename = pgref[0]
    if pagename=="-":
      # Just show a divider; nothing else
      output += "<li class='divider'></li>"
    else:
      url = pgref[1]
      if (type(url)==type([])) or (type(url)==type(())):
        # Call ourselves recursively to build a sub-menu
        output += "<li class='%s dropdown'><a href='#' class='dropdown-toggle' data-toggle='dropdown' role='button' aria-expanded='false'>%s <span class='caret'></span></a><ul class='dropdown-menu' role='menu'>%s</ul></li>" % (
          'active' if fnmatch.fnmatch(curpage, pgref[2]) else '',
          pagename,
          _generate_navbar(url, curpage)
        )
      else:
        # Create a standard menu item
        output += "<li class='%s'><a href='%s'>%s</a></li>" % (
          'active' if url==curpage else '',
          url,
          pagename
        )
  return output

@register.simple_tag(takes_context=True)
def generate_navbar(context):
  global navdata
  if navdata is None:
    try:
      # Because Block has a custom manager, the results are filtered already even before adding this filter
      contentblock = Block.objects.get(uniquetitle=NAVBAR_BLOCK_ID, datatype=Block.JSON)
    except Block.DoesNotExist:
      navdata = [['{Cannot find block with a unique title of "%s"}' % NAVBAR_BLOCK_ID, '/']]

    try:
      navdata = json.loads(contentblock.blob)
    except:
      navdata = [['{Error processing block "%s"}' % NAVBAR_BLOCK_ID, '/']]

  return _generate_navbar(navdata, context.request.path_info)

@register.simple_tag(takes_context=True)
def load_contentblock(context, uniquetitle):
  try:
    contentblock = Block.objects.get(uniquetitle=uniquetitle)
  except Block.DoesNotExist:
    blob = '{Cannot find block with a unique title of "%s"}' % uniquetitle
  else:
    blob = render_blob(contentblock.blob, contentblock.datatype)

  user = context.request.user
  if user.is_authenticated() and user.may_edit_blocks:
    blob = wrap_blob_with_editablediv(blob, uniquetitle)

  return blob
