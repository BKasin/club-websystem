from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import get_template
from django.contrib.sites.models import Site
from django.template.base import TemplateDoesNotExist

def send_template_email(request, template_prefix='default_email', extra_context=None,
                        subject=None, from_email=None, to=None, bcc=None,
                        connection=None, attachments=None, headers=None, cc=None,
                        reply_to=None):
  """
  Sends an email according to the specified template.
  The <template_prefix>.html and <template_prefix>.subj templates must both exist.
  If the <template_prefix>.txt template is missing, we'll generate a plaintext version of the html email.
  """

  current_site = Site.objects.get_current()
  context = {
    'protocol': request.scheme,
    'domain': current_site.domain,
    'site_name': current_site.name,
  }
  if extra_context: context.update(extra_context)


  if subject is None:
    #Attempt to get a subject line from its own template
    try:
      subject = ''.join(get_template(template_prefix + '.subj').render(context).splitlines())
    except TemplateDoesNotExist:
      subject = None


  # Attempt to load HTML template
  try:
    body_html = get_template(template_prefix + '.html').render(context)
    print('html = %s' % body_html)
  except TemplateDoesNotExist:
    body_html = None

  # If we succeed, and we haven't found a subject yet, extract the first line as the subject
  if (not body_html is None) and (subject is None):
    p = body_html.find('\n')
    if p >= 0:
      subject = body_html[:p]
      body_html = body_html[p+1:]

  # If we fail, we'll simply not send out an HTML version


  # Attempt to load TXT template
  try:
    body_txt = get_template(template_prefix + '.txt').render(context)
  except TemplateDoesNotExist:
    body_txt = None

  # If we succeed, and we haven't found a subject yet, extract the first line as the subject
  if not body_txt is None:
    if subject is None:
      p = body_txt.find('\n')
      if p >= 0:
        subject = body_txt[:p]
        body_txt = body_txt[p+1:]

  # If we fail, we can generate it from the HTML version
  else:
    if not body_html is None:
      import html2text
      h = html2text.HTML2Text()
      # h.ignore_links = True
      body_txt = h.handle(body_html)
    else:
      # Of course, if there's no HTML version either, then we're kind of stuck
      raise TemplateDoesNotExist('At a minumim, you must provide either %s.html or %s.txt' % (template_prefix, template_prefix))


  # Send the message
  msg = (EmailMessage if (body_html is None) else EmailMultiAlternatives)(
    subject=(subject or ''), body=body_txt, from_email=from_email, to=to, bcc=bcc,
    connection=connection, attachments=attachments, headers=headers, cc=cc,
    reply_to=reply_to
  )
  if not body_html is None: msg.attach_alternative(body_html, 'text/html')
  msg.send()
