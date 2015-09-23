#from django import template

#register = template.Library()
#register.filter('nav_tab', nav)

#@register.filter(name='nav')
def nav(section="none"):
    """Return nav menu html

    Django Template Filter that generates proper selected nav menu.
    section = current tab as string
    """


    output = """<nav class="navbar navbar-default navbar-static-top">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/home"><img alt="Brand" src="/static/img/infoseclogo.png" width="195" height="46" style='position:relative; top:-12px' /></a>
    </div>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="nav navbar-nav">
        <li class='"""

    if section == "home":
        output += "active"

    output += """'><a href='/home'>Home</a></li>
        <li class='"""

    if section == "calendar":
        output += "active"

    output += """'><a href='/calendar'>Calendar</a></li>
        <li class='"""

    if section == "projects":
        output += "active"

    output += """ dropdown'><!--Projects-->
          <a href='#' class='dropdown-toggle' data-toggle='dropdown' role='button' aria-expanded='false'>Projects <span class='caret'></span></a>
          <ul class='dropdown-menu' role='menu'>
            <li><a href='#'>Pen Test Network</a></li>
            <li><a href='#'>Raspberry Pi security system</a></li>
            <li class='divider'></li>
            <li><a href='#'>Start a project</a></li>
          </ul>
        </li>
        <li class='"""

    if section == "competitions":
        output += "active"

    output += """ dropdown'><!--Competitions-->
          <a href='#' class='dropdown-toggle' data-toggle='dropdown' role='button' aria-expanded='false'>Competitions <span class='caret'></span></a>
          <ul class='dropdown-menu' role='menu'>
            <li><a href='/pagemd/competition_ccdc'>CCDC</a></li>
            <li><a href='/pagemd/ccompetition_ncl'>NCL</a></li>
            <li><a href='/pagemd/ccompetition_itc'>ITC</a></li>
            <li><a href='/pagemd/ccompetition_nw'>NetWars</a></li>
            <li><a href='/pagemd/ccompetition_cp'>Cyber Patriot</a></li>
          </ul>
        </li>
        <li class='"""

    if section == "wiki":
        output += "active"

    output += """'><a href='#'>Wiki</a></li>
        <li class='"""

    if section == "blog":
        output += "active"

    output += """'><a href='#'>Blog</a></li>
        <li class='"""

    if section == "about":
        output += "active"

    output += """'><a href='/about' %}'>About</a></li>
      </ul>
"""

    return output
