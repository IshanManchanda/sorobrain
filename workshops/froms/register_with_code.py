from django import forms


class RegisterWithCodeForm(forms.Form):
	code = forms.CharField(label='Enter the code: ')
