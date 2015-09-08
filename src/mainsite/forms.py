from django import forms

# Form used for a user contacting a club officer
class ContactForm(forms.Form):
	full_name = forms.CharField(required=False)
	email = forms.EmailField(required=False)
	message = forms.CharField(widget=forms.Textarea)
