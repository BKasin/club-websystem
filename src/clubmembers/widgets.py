from django import forms
from django.utils.html import format_html

class PendingEmailWidget(forms.Widget):
  def render(self, name, value, attrs):
    if value:
      return format_html("""<div class="alert alert-warning" role="alert">
An activation email has been sent to <b>{}</b>.
Until that address is verified, your old email (listed above) will still be the active one.
To cancel this pending change, speak to a club officer.</div>""", value)

    else:
      return ''

class PendingEmailField(forms.Field):
  widget = PendingEmailWidget

  def __init__(self, *args, **kwargs):
    # Even if the database model marks this as required, the form should treat it as if
    # it is not, since it is a display-only field. We wouldn't want the user being asked
    # to fill in the box, when there is no box!
    kwargs.setdefault("required", False)
    super(PendingEmailField, self).__init__(*args, **kwargs)

    def bound_data(self, data, initial):
      # Always return initial because the widget doesn't render an input field.
      return initial

    def has_changed(self, initial, data):
      # Don't let this data get processed, since it's a display-only field.
      return False
