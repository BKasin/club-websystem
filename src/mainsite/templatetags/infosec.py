import json
import fnmatch

from contentblocks.models import Block

from django import template
register = template.Library()

NAVBAR_BLOCK_ID = 'navbar_infosec'
navdata = None

def generatemenu(nd, curpage):
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
          generatemenu(url, curpage)
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
def generatenav(context):
  global navdata
  if navdata is None:
    try:
      block = Block.objects.get(uniquetitle=NAVBAR_BLOCK_ID)
      navdata = json.loads(block.blob)
    except Block.DoesNotExist:
      navdata = [['Cannot find block with a unique title of "%s".' % NAVBAR_BLOCK_ID, '/']]
    except:
      navdata = [['Error processing "%s" block.' % NAVBAR_BLOCK_ID, '/']]

  return generatemenu(navdata, context.request.path_info)
