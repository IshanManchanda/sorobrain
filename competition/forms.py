import json

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import QuerySet
from django import forms

from main.models import User


class SendCertificatesForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.competition = kwargs.pop('competition')
		super(SendCertificatesForm, self).__init__(*args, **kwargs)
		self.fields['users'].queryset = User.objects.filter(
				username__in=[u for u in list(json.loads(self.competition.result).keys())])

	users = forms.ModelMultipleChoiceField(queryset=QuerySet(),
	                                       widget=FilteredSelectMultiple("Users", is_stacked=False),
	                                       required=False)
