from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import QuerySet, Q
from django import forms

from main.models import User
from workshops.models import WorkshopAccess
from workshops.models.models import WorkshopCertificate


class SendCertificatesFormWorkshop(forms.Form):
	def __init__(self, *args, **kwargs):
		self.workshop = kwargs.pop('workshop')
		super(SendCertificatesFormWorkshop, self).__init__(*args, **kwargs)
		q = User.objects.filter(~Q(username__in=[wc.user.username for wc in
		                                         WorkshopCertificate.objects.filter(
				                                         workshop=self.workshop)])).filter(
			username__in=[wa.user.username for wa in WorkshopAccess.objects.filter(workshop=self.workshop)])
		self.fields['users'].queryset = q

	users = forms.ModelMultipleChoiceField(queryset=QuerySet(),
	                                       widget=FilteredSelectMultiple("Users", is_stacked=False),
	                                       required=False)
