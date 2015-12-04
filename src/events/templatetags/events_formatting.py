from datetime import datetime, date
from django.utils import six
from django.utils.safestring import mark_safe
from django import template
register = template.Library()

TEMPLFORMAT_DATE = "%a,&nbsp;%b&nbsp;%-d&nbsp;%Y"
TEMPLFORMAT_DATETIME = "%a,&nbsp;%b&nbsp;%-d&nbsp;%Y&nbsp;%-I:%M&nbsp;%p"

@register.filter(is_safe=True)
def eventdate(dt, all_day=False):
  if isinstance(dt, datetime):
    if all_day:
      return mark_safe(dt.strftime(TEMPLFORMAT_DATE))
    else:
      return mark_safe(dt.strftime(TEMPLFORMAT_DATETIME))
  elif isinstance(dt, date):
    return mark_safe(dt.strftime(TEMPLFORMAT_DATE))

@register.filter
def eventid(id):
  if isinstance(id, six.integer_types):
    return "#%s" % id
  else:
    return "-"
