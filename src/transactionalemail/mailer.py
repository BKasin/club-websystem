from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.sites.models import Site

def send_template_email(request, template_prefix, to, from_email=None, reply_to=None, extra_context=None):
  current_site = Site.objects.get_current()
  context = {
    'protocol': request.scheme,
    'domain': current_site.domain,
    'site_name': current_site.name,
  }
  if extra_context: context.update(extra_context)
  template_subj = get_template(template_prefix + '.subj')
  template_txt = get_template(template_prefix + '.txt')
  template_html = get_template(template_prefix + '.html')
  msg = EmailMultiAlternatives(
    subject=''.join(template_subj.render(context).splitlines()),
    body=template_txt.render(context),
    from_email=from_email,
    to=to,
    reply_to=reply_to
  )
  msg.attach_alternative(template_html.render(context), 'text/html')
  msg.send()
