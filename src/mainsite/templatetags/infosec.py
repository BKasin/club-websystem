import fnmatch

from django import template
register = template.Library()

navdata = (
  ("Home", "/"),
  ("Calendar", "/calendar/"),
  ("Projects", (
    ("Pen Test Network", "/project/pentest/"),
    ("Raspberry Pi security system", "/project/rpi/"),
    ("-"),
    ("Start a project", "/startaproject/"),
  ), "/pagemd/project_*"),
  ("Competitions", (
    ("CCDC", "/pagemd/competition_ccdc/"),
    ("NCL", "/pagemd/competition_ncl/"),
    ("ITC", "/pagemd/competition_itc/"),
    ("Netwars", "/pagemd/competition_nw/"),
    ("Cyber Patriot", "/pagemd/competition_cp/"),
  ), "/pagemd/competition_*"),
  ("Wiki", "#"),
  ("Blog", "#"),
  ("About", "/about/"),
)

def generatemenu(nd, curpage):
  output = ""
  for pgref in nd:
    pagename = pgref[0]
    if pagename=="-":
      # Just show a divider; nothing else
      output += "<li class='divider'></li>"
    else:
      url = pgref[1]
      if type(url)==type(()):
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
  return generatemenu(navdata, context.request.path_info)
