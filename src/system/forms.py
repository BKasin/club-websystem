from django import forms

# Form used for a user contacting a club officer
class ContactForm(forms.Form):
	full_name = forms.CharField(label='Full name', required=False)
	email = forms.EmailField(label='Your email', required=False)
	message = forms.CharField(label='Message', widget=forms.Textarea)
